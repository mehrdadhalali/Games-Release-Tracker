"""This script is for getting the emails of the subscribers for each genre."""

from os import environ as ENV

from boto3 import client
from dotenv import load_dotenv

load_dotenv()

# pylint: disable = C0103


def create_SNS_topic_object(topic_arn: str) -> dict:
    """Given an ARN, returns a dictionary containing a topic's genre as well."""

    return {
        "topic_arn": topic_arn,
        "genre": topic_arn.split(":")[-1].split("-")[-1]
    }


def get_SNS_topics(sns: client) -> list[dict]:
    """Returns all of the SNS topics from AWS."""

    all_sns_topics = sns.list_topics()["Topics"]

    games_sns_topics = [topic
                        for topic in all_sns_topics
                        if ENV["SNS_TOPIC_PREFIX"] in topic["TopicArn"]]

    return [create_SNS_topic_object(topic["TopicArn"])
            for topic in games_sns_topics]


def get_subscribers_per_genre() -> list[dict]:
    """Returns all of the subscriber emails for each genre."""

    sns = client(service_name="sns",
                 aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                 aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    topics = get_SNS_topics(sns)

    subscribers_per_genre = []
    for topic in topics:

        subscription_list = sns.list_subscriptions_by_topic(
            TopicArn=topic["topic_arn"]
        )["Subscriptions"]

        subscribers_per_genre.append({
            "genre": topic["genre"],
            "subscribers": [subscription["Endpoint"]
                            for subscription
                            in subscription_list
                            if subscription["SubscriptionArn"] != "PendingConfirmation"]
        })

    return subscribers_per_genre
