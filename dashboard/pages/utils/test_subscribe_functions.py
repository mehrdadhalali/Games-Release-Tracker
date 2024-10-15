"""This is the test file for subscribe_functions.py."""

from unittest.mock import patch, MagicMock

import pytest
import pandas as pd

from subscribe_functions import (
    is_email_in_rds,
    add_subscriber_to_rds,
    get_subscriber_counts,
    create_subscriber_chart,
    subscribe_user_to_topics
)

# Mock data
MOCK_EMAIL = "test@example.com"
MOCK_NAME = "Test User"
MOCK_TOPIC = "c13-games-action"
mock_genres = ["Action", "Adventure"]


@pytest.fixture
def mock_connect_rds():
    """Mocks a connection to RDS."""
    with patch("subscribe_functions.connect_rds") as mock:
        yield mock


@pytest.fixture
def mock_sns_client():
    """Mocks the SNS client."""
    with patch("subscribe_functions.sns_client") as mock:
        yield mock


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


def test_get_subscriber_counts(mock_sns_client):
    """Tests fetching subscriber counts from SNS."""
    mock_sns_client.list_topics.return_value = {
        'Topics': [{'TopicArn': 'arn:aws:sns:us-east-1:123456789012:c13-games-action'}]
    }
    mock_sns_client.get_topic_attributes.return_value = {
        'Attributes': {'SubscriptionsConfirmed': '5'}
    }

    df = get_subscriber_counts("c13-games")
    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 1
    assert df['Subscribers'][0] == 5


def test_create_subscriber_chart():
    """Tests the creation of a subscriber chart."""
    chart = create_subscriber_chart('c13-games')
    assert chart is not None  # More specific checks can be added


def test_subscribe_user_to_topics(mock_sns_client):
    """Tests adding an email to an SNS topic."""
    mock_sns_client.list_topics.return_value = {
        'Topics': [
            {'TopicArn': f'arn:aws:sns:us-east-1:123456789012:c13-games-{genre.lower()}'}
              for genre in mock_genres]
    }
    mock_sns_client.subscribe.return_value = {'SubscriptionArn': 'mock-arn'}

    subscribe_user_to_topics(MOCK_EMAIL, mock_genres)
    assert mock_sns_client.subscribe.call_count == len(mock_genres)
