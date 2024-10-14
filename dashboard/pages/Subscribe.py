"""
This page includes the functionality for users to subscribe
and unsubscribe to email updates about game releases.
"""

import re
from os import environ as ENV

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
    """Creates a horisontal bar chart about subscriber counts to SNS topics."""
    data = get_subscriber_counts(topic)  # Subscriber counts

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

st.title("Subscribe to Games Tracker")

st.write("""Subscribe to stay updated! Select the types of content
          you're interested in, and we'll send you personalised email
          updates based on your preferences.""")

st.divider()

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

cols = st.columns([1, 2, 1])
with cols[1]:
    st.write(" <br> ", unsafe_allow_html=True)

    email = st.text_input("Enter your email:")

    if st.button("Subscribe"):
        if re.match(email_pattern, email):
            st.success(f"You are subscribed with {email}. Bosh!")
        else:
            st.warning("Please enter a valid email address.")
    
    st.markdown("<small>* NSFW content is not included in emails.</small>",
                unsafe_allow_html=True)

st.divider()

cols = st.columns([0.5, 2, 0.5])
with cols[1]:
    st.altair_chart(create_subscriber_chart("c13-games"), use_container_width=True)

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
