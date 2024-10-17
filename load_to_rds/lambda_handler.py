"""The script that gets called from the lambda."""

from json import loads

from upload_to_db import load_to_db
from email_subscribers import send_genre_emails

# pylint: disable=W0613


def lambda_handler(event, session):
    """The lambda handler.
        Event should be a list of inputs from other lambdas."""

    scraped_data = []

    for output in event:

        data = output["body"]["data"]

        if not isinstance(data, dict):
            data = loads(data)

        scraped_data.append(data)

    load_to_db(scraped_data)
    send_genre_emails(scraped_data)
