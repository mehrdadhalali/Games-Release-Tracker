"""This script is for emailing the subscribers using SES."""

from os import environ as ENV

from boto3 import client
from dotenv import load_dotenv

from create_html_message import create_html, format_genre_text
from get_subscriber_emails import get_subscribers_per_genre

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


def send_genre_emails(scraped_data: list[dict]):
    """Sends emails to the genre subscribers."""

    ses = client(service_name="ses",
                 aws_access_key_id=ENV["MY_AWS_ACCESS_KEY"],
                 aws_secret_access_key=ENV["MY_AWS_SECRET_ACCESS_KEY"])

    subscribers_per_genre = get_subscribers_per_genre()

    for item in subscribers_per_genre:

        if len(item["subscribers"]) > 0:

            genre = item["genre"]
            genre_games = get_games_by_genre(genre, scraped_data)
            if len(genre_games) > 0:
                to_send = create_html(genre_games, genre)

                subscriber_emails = item["subscribers"]

                ses.send_email(
                    Source=ENV["SENDER_EMAIL_ADDRESS"],
                    Destination={"ToAddresses": subscriber_emails,
                                 "BccAddresses": [],
                                 "CcAddresses": []},
                    Message={
                        "Subject": {
                            "Data": f"New {format_genre_text(genre)} games for you!"
                        },
                        "Body": {
                            "Html": {
                                "Data": to_send
                            }
                        }
                    })
