"""The script that gets called from the lambda."""

from json import load

from upload_to_db import load_to_db
from update_sns_topics import update_SNS_topics


def lambda_handler(event, session):
    """The lambda handler.
        Event should be a list of inputs from other lambdas."""

    scraped_data = [output["body"]
                    for output in event]

    load_to_db(scraped_data)
    update_SNS_topics(scraped_data)
