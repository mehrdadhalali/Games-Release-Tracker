"""Script for the AWS lambda handler."""

from datetime import datetime
from json import dumps

from scrape_gog import get_games_for_the_day


def lambda_handler(event, context):  # pylint: disable=W0613
    """The main Lambda function"""

    games_list = get_games_for_the_day(datetime.today())

    return dumps({
        "statusCode": 200,
        "body": {
            "data": games_list
        }
    })
