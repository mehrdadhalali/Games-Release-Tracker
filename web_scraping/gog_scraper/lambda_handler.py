"""Script for the AWS lambda handler."""

from datetime import datetime

from scrape_gog import get_games_for_the_day


def lambda_handler(event, context):  # pylint: disable=W0613
    """The main Lambda function"""

    dates = [datetime(2024, 10, 8)]

    games_list = get_games_for_the_day(dates[0])

    if len(dates) > 1:

        for day in dates[1:]:
            games_list["listings"].extend(get_games_for_the_day(day))

    print("Games added: ")
    for listing in games_list["listings"]:
        print(listing["title"])

    return {
        "statusCode": 200,
        "body": {
            "data": games_list
        }
    }
