"""The main script to handle the emailing of reports to subscribers."""

from os import environ as ENV
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.mime.text import MIMEText

from boto3 import client
from dotenv import load_dotenv

from database_handler import get_subscriber_info
from generate_report import create_report


def get_subscriber_first_name(subscriber_name: str) -> str:
    """Returns a subscribers first name."""
    return subscriber_name.split(" ")[0].title()


def email_summary_report(ses_client: client, first_name: str, recipient: str, report: bytes):
    """Sends an email with a PDF report attachment to a recipient."""
    msg = MIMEMultipart()
    msg['Subject'] = "Your weekly gaming industry report."
    msg['From'] = ENV['FROM_EMAIL']
    msg['To'] = recipient
    body_text = f"Hi, {
        first_name}! Please find attached your weekly report summary."

    msg.attach(MIMEText(body_text, 'plain'))
    pdf_attachment = MIMEBase('application', 'octet-stream')
    pdf_attachment.set_payload(report)
    encoders.encode_base64(pdf_attachment)
    pdf_attachment.add_header('Content-Disposition',
                              'attachment; filename="summary_report.pdf"')
    msg.attach(pdf_attachment)

    ses_client.send_raw_email(
        Source=ENV['FROM_EMAIL'],
        Destinations=[recipient],
        RawMessage={
            'Data': msg.as_string(),
        })


def generate_and_send_report():
    """Generates the summary report and sends it to each subscriber."""
    load_dotenv()
    summary_report = create_report()
    mail_client = client('ses', region_name=ENV['AWS_REGION_NAME'],
                         aws_access_key_id=ENV['MY_AWS_ACCESS_KEY'],
                         aws_secret_access_key=ENV['MY_AWS_SECRET_KEY'],)
    sub_info = get_subscriber_info()
    for subscriber in sub_info:
        name = get_subscriber_first_name(subscriber)
        email_summary_report(
            mail_client, name, sub_info[subscriber], summary_report)
