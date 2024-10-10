"""Script run when the AWS Lambda is triggered."""

from email_report import generate_and_send_report
from database_handler import get_genre_listing_count, get_platform_listing_count, \
    get_platform_average_price, get_free_to_play

# pylint: disable=W0613


def lambda_handler(event, context):
    """Function run when AWS Lambda is triggered."""
    genre_dict = get_genre_listing_count()
    platform_dict = get_platform_listing_count()
    total_games = sum(platform_dict.values())
    total_platforms = len(platform_dict.keys())
    platform_price = get_platform_average_price()
    free_games = get_free_to_play()
    generate_and_send_report(total_games, total_platforms,
                             genre_dict, platform_price, platform_dict, free_games)
    return {"statusCode": 200}
