"""The script that gets called from the lambda."""

from json import loads

from upload_to_db import load_to_db

# pylint: disable=W0613


def lambda_handler(event, session):
    """The lambda handler.
        Event should be a list of inputs from other lambdas."""

    scraped_data = []

    for output in event:

        data = loads(output["body"]["data"])

        if not isinstance(data, dict):
            data = loads(data)

        scraped_data.append(data)

    load_to_db(scraped_data)
