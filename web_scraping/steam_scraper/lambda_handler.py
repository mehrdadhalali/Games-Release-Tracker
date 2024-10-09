"""Script for the AWS lambda handler."""

from datetime import datetime

from scrape_steam import collect_and_parse_games

# pylint: disable=W0613


def lambda_handler(event, context):
    """Triggered with the lambda. Optional time argument can be
    passed in event: 'time'."""
    time_arg = event.get('time', None)
    if isinstance(time_arg, str):
        try:
            time_arg = datetime.fromisoformat(time_arg)
        except ValueError:
            time_arg = datetime.now()
    else:
        time_arg = datetime.now()

    listings = collect_and_parse_games(time_arg)
    return {
        'statusCode': 200,
        'body': {
            'data': listings
        }
    }
