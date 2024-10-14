"""
This page includes the functionality for users to subscribe
and unsubscribe to email updates about game releases.
"""

import re
from os import environ as ENV

import psycopg2
from boto3 import client
import pandas as pd
import altair as alt
import streamlit as st
from dotenv import load_dotenv

# Regex for validating email
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

st.set_page_config(layout="wide")

load_dotenv()

# Initialize the boto3 SNS client
sns_client = client('sns', region_name=ENV["REGION"])


def connect_rds():  # Initialize PostgreSQL connection
    conn = psycopg2.connect(
        host=ENV["DB_HOST"],
        database=ENV["DB_NAME"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASSWORD"],
        port=ENV["DB_PORT"]
    )
    return conn


def is_email_in_rds(email):
    """Check if the email is already subscribed to the weekly report."""
    try:
        conn = connect_rds()
        if conn is not None:
            cur = conn.cursor()
            query = "SELECT sub_id FROM subscriber WHERE sub_email = %s;"
            cur.execute(query, (email,))
            result = cur.fetchone()
            cur.close()
            conn.close()
            return result is not None
    except Exception as e:
        st.error(f"Error checking email in RDS: {e}")
        return False


def add_subscriber_to_rds(name, email):
    """Insert subscriber name and email into the RDS database if not already present."""
    if is_email_in_rds(email):
        st.warning(f"{email} is already subscribed to the weekly report.")
        return

    try:
        conn = connect_rds()
        cur = conn.cursor()
        query = """
        INSERT INTO subscriber (sub_name, sub_email)
        VALUES (%s, %s)
        ON CONFLICT (sub_email) DO NOTHING;
        """
        cur.execute(query, (name, email))
        conn.commit()
        cur.close()
        conn.close()
        st.success(f"{name} has been subscribed to the weekly report.")
    except Exception as e:
        st.error(f"Error adding subscriber to RDS: {e}")


def get_subscriber_counts(topic_startswith):
    """Get subscriber counts for all relevant topics."""
    response = sns_client.list_topics()
    topic_arns = response['Topics']

    subscriber_data = []
    for topic in topic_arns:
        topic_arn = topic['TopicArn']
        if topic_startswith in topic_arn:
            # Get subscription attributes for this topic
            attributes = sns_client.get_topic_attributes(TopicArn=topic_arn)
            subscriber_count = int(
                attributes['Attributes']['SubscriptionsConfirmed'])
            topic_name = topic_arn.split(
                ":")[-1].replace(topic_startswith + "-", "").title()
            subscriber_data.append(
                {'Topic': topic_name, 'Subscribers': subscriber_count})

    return pd.DataFrame(subscriber_data)


def create_subscriber_chart(topic):
    """Creates a horizontal bar chart about subscriber counts to SNS topics."""
    data = get_subscriber_counts(topic)

    chart = alt.Chart(data).mark_bar(color="#6a0dad").encode(
        x=alt.X('Subscribers:Q', axis=alt.Axis(format='d')),
        y=alt.Y('Topic:N', sort='-x')
    ).properties(
        title=alt.TitleParams(
            text='Subscriber Counts for Game Genres',
            anchor='middle',
            fontSize=17
        )
    )

    return chart


def is_email_in_sns_topic(email, topic_arn):
    """Check if the email is already subscribed to the given SNS topic."""
    try:
        subscriptions = sns_client.list_subscriptions_by_topic(
            TopicArn=topic_arn)
        for sub in subscriptions['Subscriptions']:
            if sub['Endpoint'] == email:
                return True
        return False
    except Exception as e:
        st.error(f"Error checking SNS topic subscription: {e}")
        return False


def subscribe_user_to_topics(email, selected_genres):
    """Subscribe user to the selected SNS topics, checking for duplicates."""
    topic_prefix = "c13-games"
    for genre in selected_genres:
        topic_name = f"{topic_prefix}-{genre.lower()}"
        response = sns_client.list_topics()
        topic_arn = None

        # Find the ARN for the topic
        for topic in response['Topics']:
            if topic_name in topic['TopicArn']:
                topic_arn = topic['TopicArn']
                break

        if topic_arn:
            if not is_email_in_sns_topic(email, topic_arn):
                sns_client.subscribe(
                    TopicArn=topic_arn,
                    Protocol='email',
                    Endpoint=email
                )
                st.success(f"Subscribed to {genre} topic.")
            else:
                st.warning(f"Already subscribed to {genre} topic.")
        else:
            st.warning(f"Topic {topic_name} not found.")


st.title("Subscribe to Games Tracker")

st.write("""Subscribe to stay updated! Select the types of content
          you're interested in, and we'll send you personalised email
          updates based on your preferences.""")

st.divider()

# Mapping genres to SNS topics
genre_topics = {
    "Indie": "indie",
    "Action": "action",
    "Casual": "casual",
    "Adventure": "adventure",
    "Simulation": "simulation",
    "RPG": "rpg",
    "Strategy": "strategy",
    "Sports": "sports",
    "Racing": "racing",
    "Multiplayer": "multiplayer"
}

cols = st.columns([1, 2])
with cols[0]:
    st.write("Receive our weekly report:")
with cols[1]:
    st.write("New game releases:")

cols = st.columns([1, 1, 1])
with cols[0]:
    weekly_report = st.checkbox("Weekly Report")

with cols[1]:
    indie = st.checkbox("Indie")
    action = st.checkbox("Action")
    casual = st.checkbox("Casual")
    adventure = st.checkbox("Adventure")
    simulation = st.checkbox("Simulation")

with cols[2]:
    rpg = st.checkbox("RPG")
    strategy = st.checkbox("Strategy")
    sports = st.checkbox("Sports")
    racing = st.checkbox("Racing")
    multiplayer = st.checkbox("Multiplayer")

# Get the selected genres
selected_genres = [genre for genre, checked in genre_topics.items(
) if st.session_state.get(checked)]

cols = st.columns([1, 2, 1])
with cols[1]:
    st.write(" <br> ", unsafe_allow_html=True)

    # Name input field
    name = st.text_input("Enter your name:")

    email = st.text_input("Enter your email:")

    if st.button("Subscribe"):
        if re.match(email_pattern, email):
            if weekly_report:
                if name:
                    add_subscriber_to_rds(name, email)
                else:
                    st.warning("Please enter your name to subscribe.")
            if selected_genres:  # Subscribe to selected genres
                subscribe_user_to_topics(email, selected_genres)
        else:
            st.warning("Please enter a valid email address.")

    st.markdown("<small>* NSFW content is not included in emails.</small>",
                unsafe_allow_html=True)

st.divider()

cols = st.columns([0.5, 2, 0.5])
with cols[1]:
    st.altair_chart(create_subscriber_chart(
        "c13-games"), use_container_width=True)

st.divider()

cols = st.columns([1, 2, 1])
with cols[1]:
    unsubscribe_expander = st.expander("Unsubscribe", expanded=False)

    unsubscribe_email = unsubscribe_expander.text_input(
        "Enter your email:", key="unsubscribe")

    if unsubscribe_expander.button("Unsubscribe"):
        if re.match(email_pattern, unsubscribe_email):
            unsubscribe_expander.success(
                f"You have unsubscribed {unsubscribe_email}.")
        else:
            unsubscribe_expander.warning("Please enter a valid email address.")
