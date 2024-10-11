"""This script is for updating the SNS topics with the right HTML messages."""

from json import load
from os import environ as ENV

from boto3 import client
from dotenv import load_dotenv

from create_sns_topics import create_topics
from create_ugly_topic_message import create_ugly_disgusting_message_i_hate_it

load_dotenv()


def get_games_by_genre(genre: str, scraped_data: list[dict]) -> list[dict]:
    """Given a genre, returns all games with that genre."""

    genre_games = []

    for website in scraped_data:
        for game in website["listings"]:
            if any(genre in game_genre.lower()
                   for game_genre in game["genres"]):
                genre_games.append(game)

    return genre_games


def update_SNS_topics(topics: list[dict],
                      scraped_data: list[dict]):

    sns = client(service_name="sns",
                 aws_access_key_id=ENV["AWS_ACCESS_KEY"],
                 aws_secret_access_key=ENV["AWS_SECRET_ACCESS_KEY"])

    for topic in topics:

        genre = topic["genre"]
        games_of_genre = get_games_by_genre(genre, scraped_data)

        if len(games_of_genre) > 0:
            email_contents = create_ugly_disgusting_message_i_hate_it(
                games_of_genre, genre)

            sns.publish(
                TopicArn=topic["topic_arn"],
                Message=email_contents,
                Subject=f"New {genre} Games Released!!"
            )


if __name__ == "__main__":

    with open("topics.json", "r") as f:
        topics = load(f)

    with open("gog_data.json", "r") as f:
        gog_games = load(f)

    with open("steam_data.json", "r") as f:
        steam_games = load(f)

    update_SNS_topics(topics, [gog_games, steam_games])
