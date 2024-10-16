"""This script includes functions used in Subscribe.py."""

from os import environ as ENV

import psycopg2
from boto3 import client
import pandas as pd
import altair as alt
import streamlit as st
from dotenv import load_dotenv


load_dotenv()

sns_client = client('sns', region_name=ENV["REGION"])

def connect_rds():
    """Initialize PostgreSQL connection."""
    return psycopg2.connect(
        host=ENV["DB_HOST"],
        database=ENV["DB_NAME"],
        user=ENV["DB_USER"],
        password=ENV["DB_PASSWORD"],
        port=ENV["DB_PORT"]
    )


def is_email_in_rds(email):
    """Check if the email is already subscribed to the weekly report."""
    with connect_rds() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT sub_id FROM subscriber WHERE sub_email = %s;", (email,))
            return cur.fetchone() is not None


def add_subscriber_to_rds(name, email):
    """Insert subscriber name and email into the RDS database if not already present."""
    if is_email_in_rds(email):
        st.warning(f"{email} is already subscribed to the weekly report.")
        return

    with connect_rds() as conn:
        with conn.cursor() as cur:
            cur.execute("""
            INSERT INTO subscriber (sub_name, sub_email)
            VALUES (%s, %s)
            ON CONFLICT (sub_email) DO NOTHING;
            """, (name, email))
            conn.commit()
            st.success(f"{name} has been subscribed to the weekly report.")


def get_subscriber_counts(topic_startswith):
    """Get subscriber counts for all relevant topics."""
    response = sns_client.list_topics()
    topic_arns = response['Topics']

    subscriber_data = []
    for topic in topic_arns:
        topic_arn = topic['TopicArn']
        if topic_startswith in topic_arn:
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
    subscriptions = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
    return any(sub['Endpoint'] == email for sub in subscriptions['Subscriptions'])


def subscribe_user_to_topics(email, selected_genres):
    """Subscribe user to the selected SNS topics, checking for duplicates."""
    topic_prefix = "c13-games"
    for genre in selected_genres:
        topic_name = f"{topic_prefix}-{genre.lower()}"
        response = sns_client.list_topics()
        topic_arn = None

        for topic in response['Topics']:
            if topic_name in topic['TopicArn']:
                topic_arn = topic['TopicArn']
                break

        if topic_arn and not is_email_in_sns_topic(email, topic_arn):
            sns_client.subscribe(
                TopicArn=topic_arn,
                Protocol='email',
                Endpoint=email
            )
            st.success(f"Successfully subscribed to {
                       genre} topic. Check your email to confirm the subscription.")
        else:
            st.warning(f"Already subscribed to {genre}.")


def get_sns_topics_with_prefix(prefix):
    """Return all SNS topics that start with the given prefix."""
    response = sns_client.list_topics()
    return [topic['TopicArn'] for topic in response['Topics'] if prefix in topic['TopicArn']]


def get_user_subscriptions_for_topic(topic_arn, email):
    """Return the subscription ARN if the user is subscribed to the topic."""
    subscriptions = sns_client.list_subscriptions_by_topic(TopicArn=topic_arn)
    for sub in subscriptions['Subscriptions']:
        if sub['Endpoint'] == email and sub['SubscriptionArn'].startswith("arn:aws:sns"):
            return sub['SubscriptionArn']
    return None


def unsubscribe_user_from_topic(subscription_arn):
    """Unsubscribe user from the topic using the subscription ARN."""
    sns_client.unsubscribe(SubscriptionArn=subscription_arn)


def unsubscribe_user_from_all_topics(email):
    """Unsubscribe user from all SNS topics that start with 'c13-games'."""
    topic_prefix = "c13-games"
    unsubscribed_topics = []

    topics = get_sns_topics_with_prefix(topic_prefix)

    for topic_arn in topics:
        subscription_arn = get_user_subscriptions_for_topic(topic_arn, email)
        if subscription_arn:
            unsubscribe_user_from_topic(subscription_arn)
            unsubscribed_topics.append(topic_arn.split(
                ":")[-1].replace(topic_prefix + "-", "").title())

    if unsubscribed_topics:
        st.success(f"Unsubscribed from the following topics: {
                   ', '.join(unsubscribed_topics)}.")
    else:
        st.warning("No subscriptions found for the email.")


def remove_subscriber_from_rds(email):
    """Remove the subscriber from the RDS database."""
    with connect_rds() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "DELETE FROM subscriber WHERE sub_email = %s;", (email,))
            conn.commit()
            st.success(
                f"{email} has been unsubscribed from the weekly report.")
