"""This script is for creating SNS topics for each genre."""

from os import environ as ENV

from boto3 import client
from dotenv import load_dotenv

load_dotenv()

GENRES = [
    'indie',
    'action',
    'casual',
    'adventure',
    'simulation',
    'rpg',
    'strategy',
    'sports',
    'racing',
    'multiplayer']


def create_topics(genres: list) -> list[dict]:
    """Creates an SNS topic for every genre, returns their names and ARNs."""

    sns = client(service_name="sns",
                 aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                 aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    topics = []

    for genre in genres:
        response = sns.create_topic(
            Name=f"{ENV["SNS_TOPIC_PREFIX"]}{genre.lower()}")
        topics.append({
            "genre": genre,
            "topic_arn": response["TopicArn"]
        })

    return topics


if __name__ == "__main__":

    create_topics(GENRES)
