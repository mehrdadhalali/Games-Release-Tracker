"""This is the test file for subscribe_functions.py."""
# pylint: skip-file

from unittest.mock import patch, MagicMock
import os

import pytest
import pandas as pd

from subscribe_functions import (
    is_email_in_rds,
    add_subscriber_to_rds,
    get_subscriber_counts,
    create_subscriber_chart
)

# Mock data
MOCK_EMAIL = "test@example.com"
MOCK_NAME = "Test User"
MOCK_TOPIC = "c13-games-action"
mock_genres = ["Action", "Adventure"]


@pytest.fixture(autouse=True)
def mock_env_vars():
    """Mocks environment variables."""
    with patch.dict(os.environ, {"REGION": "us-east-1"}):
        yield


@pytest.fixture
def mock_connect_rds():
    """Mocks a connection to RDS."""
    with patch("subscribe_functions.connect_rds") as mock:
        yield mock


@pytest.fixture
def mock_boto3_client():
    """Mocks the boto3 SNS client."""
    with patch("subscribe_functions.boto3.client") as mock_boto3_client:
        mock_sns_client = MagicMock()
        mock_boto3_client.return_value = mock_sns_client
        yield mock_sns_client


def test_is_email_in_rds(mock_connect_rds):
    """Tests checking if email is already in RDS."""
    mock_cursor = MagicMock()
    mock_connect_rds.return_value.__enter__.return_value.cursor.return_value = mock_cursor

    mock_cursor.fetchone.return_value = (1,)  # Simulating an existing email
    result = is_email_in_rds(MOCK_EMAIL)
    assert result is True


def test_add_subscriber_to_rds(mock_connect_rds):
    """Tests inserting to RDS subscriber table."""
    mock_cursor = MagicMock()
    mock_connect_rds.return_value.__enter__.return_value.cursor.return_value = mock_cursor

    # Simulate email already subscribed
    mock_cursor.fetchone.return_value = (1,)
    add_subscriber_to_rds(MOCK_NAME, MOCK_EMAIL)
    mock_cursor.execute.assert_not_called()  # No insert should occur


def test_get_subscriber_counts(mock_boto3_client):
    """Tests fetching subscriber counts from SNS."""
    mock_boto3_client.list_topics.return_value = {
        'Topics': [{'TopicArn': 'arn:aws:sns:us-east-1:123456789012:c13-games-action'}]
    }
    mock_boto3_client.get_topic_attributes.return_value = {
        'Attributes': {'SubscriptionsConfirmed': '5'}
    }

    df = get_subscriber_counts("c13-games")

    assert isinstance(df, pd.DataFrame)

    assert df.shape[0] == 10



def test_create_subscriber_chart():
    """Tests the creation of a subscriber chart."""
    chart = create_subscriber_chart('c13-games')
    assert chart is not None  # More specific checks can be added
