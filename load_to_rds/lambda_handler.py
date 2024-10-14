"""The script that gets called from the lambda."""

from json import load

from upload_to_db import load_to_db


def lambda_handler(event, session):
    """The lambda handler.
        Event should be a list of inputs from other lambdas."""

    scraped_data = [output["body"]["data"]
                    for output in event]

    load_to_db(scraped_data)
