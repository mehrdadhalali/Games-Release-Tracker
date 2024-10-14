"""This script is for updating the SNS topics with the right HTML messages."""

from os import environ as ENV

from boto3 import client
from dotenv import load_dotenv

from create_topic_message import create_text_message, format_genre_text

load_dotenv()

# pylint: disable = C0103

def get_games_by_genre(genre: str, scraped_data: list[dict]) -> list[dict]:
    """Given a genre, returns all games with that genre."""

    genre_games = []

    for website in scraped_data:
        for game in website["listings"]:
            if any(genre in game_genre.lower()
                   for game_genre in game["genres"]):
                genre_games.append(game)

    return genre_games


def create_SNS_topic_object(topic_arn: str) -> dict:
    """Given an ARN, returns a dictionary containing a topic's genre as well."""

    return {
        "topic_arn": topic_arn,
        "genre": topic_arn.split(":")[-1].split("-")[-1]
    }


def get_SNS_topics() -> list[dict]:
    """Returns all of the SNS topics from AWS."""

    sns = client(service_name="sns",
                 aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                 aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    all_sns_topics = sns.list_topics()["Topics"]

    games_sns_topics = [topic
                        for topic in all_sns_topics
                        if ENV["SNS_TOPIC_PREFIX"] in topic["TopicArn"]]

    return [create_SNS_topic_object(topic["TopicArn"])
            for topic in games_sns_topics]


def update_SNS_topics(scraped_data: list[dict]):
    """Updates the SNS topics with the right messages."""

    topics = get_SNS_topics()

    sns = client(service_name="sns",
                 aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                 aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    for topic in topics:

        genre = topic["genre"]
        games_of_genre = get_games_by_genre(genre, scraped_data)

        if len(games_of_genre) > 0:
            email_contents = create_text_message(
                games_of_genre, genre)

            sns.publish(
                TopicArn=topic["topic_arn"],
                Message=email_contents,
                Subject=f"New {format_genre_text(genre)} Games Released!!"
            )
