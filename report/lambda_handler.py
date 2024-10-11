"""Script run when the AWS Lambda is triggered."""

from email_report import generate_and_send_report

# pylint: disable=W0613


def lambda_handler(event, context):
    """Function run when AWS Lambda is triggered."""
    generate_and_send_report()
    return {"statusCode": 200}
