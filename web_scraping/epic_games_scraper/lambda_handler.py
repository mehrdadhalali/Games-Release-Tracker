"""Script that runs when AWS Lambda is triggered."""

from extract_epic import process_listings

# pylint: disable=W0613


def lambda_handler(event, context):
    """Entry-point for the AWS Lambda."""
    listings = process_listings()
    return {"statusCode": 200,
            "body": {
                "data": listings}
            }
