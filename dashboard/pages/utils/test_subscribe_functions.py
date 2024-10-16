"""This is the test file for subscribe_functions.py."""
# pylint: skip-file

import pytest
from unittest.mock import patch
import pandas as pd
from subscribe_functions import (
    get_subscriber_counts,
    subscribe_user_to_topics,
    unsubscribe_user_from_all_topics,
)

@pytest.fixture
def mock_boto3_client():
    """Mocks the boto3 client."""
    with patch('boto3.client') as mock_client:
        yield mock_client


def test_get_subscriber_counts(mock_boto3_client):
    """Tests fetching subscriber counts from SNS."""
    # Mock SNS response for list_topics
    mock_boto3_client.return_value.list_topics.return_value = {
        'Topics': [
            {'TopicArn': 'arn:aws:sns:us-east-1:123456789012:c13-games-action'},
            {'TopicArn': 'arn:aws:sns:us-east-1:123456789012:c13-games-adventure'}
        ]
    }

    # Mock response for get_topic_attributes
    mock_boto3_client.return_value.get_topic_attributes.side_effect = [
        {'Attributes': {'SubscriptionsConfirmed': '5'}},
        {'Attributes': {'SubscriptionsConfirmed': '10'}}
    ]

    df = get_subscriber_counts(mock_boto3_client.return_value, "c13-games")

    assert isinstance(df, pd.DataFrame)
    assert df.shape[0] == 2
    assert df.loc[0, 'Topic'] == "Action"
    assert df.loc[0, 'Subscribers'] == 5
    assert df.loc[1, 'Topic'] == "Adventure"
    assert df.loc[1, 'Subscribers'] == 10


def test_subscribe_user_to_topics(mock_boto3_client):
    """Tests adding an email to multiple SNS topics."""
    mock_genres = ['Action', 'Adventure']

    # Mock list_topics
    mock_boto3_client.return_value.list_topics.return_value = {
        'Topics': [
            {'TopicArn': 'arn:aws:sns:us-east-1:123456789012:c13-games-action'},
            {'TopicArn': 'arn:aws:sns:us-east-1:123456789012:c13-games-adventure'}
        ]
    }

    # Mock is_email_in_sns_topic to always return False
    mock_boto3_client.return_value.list_subscriptions_by_topic.return_value = {
        'Subscriptions': []
    }

    # Mock subscribe function
    mock_boto3_client.return_value.subscribe.return_value = {
        'SubscriptionArn': 'mock-arn'}

    subscribe_user_to_topics(
        mock_boto3_client.return_value, "test@example.com", mock_genres)

    # Ensure subscribe is called twice (for both genres)
    assert mock_boto3_client.return_value.subscribe.call_count == len(
        mock_genres)


def test_unsubscribe_user_from_all_topics(mock_boto3_client):
    """Tests unsubscribing user from all SNS topics."""
    email = "test@example.com"

    # Mock list_topics
    mock_boto3_client.return_value.list_topics.return_value = {
        'Topics': [
            {'TopicArn': 'arn:aws:sns:us-east-1:123456789012:c13-games-action'},
            {'TopicArn': 'arn:aws:sns:us-east-1:123456789012:c13-games-adventure'}
        ]
    }

    # Mock list_subscriptions_by_topic
    mock_boto3_client.return_value.list_subscriptions_by_topic.side_effect = [
        {'Subscriptions': [
            {'Endpoint': email, 'SubscriptionArn': 'arn:aws:sns:us-east-1:sub-action'}]},
        {'Subscriptions': [
            {'Endpoint': email, 'SubscriptionArn': 'arn:aws:sns:us-east-1:sub-adventure'}]}
    ]

    # Mock unsubscribe function
    mock_boto3_client.return_value.unsubscribe.return_value = {}

    unsubscribe_user_from_all_topics(mock_boto3_client.return_value, email)

    # Ensure unsubscribe is called for both topics
    assert mock_boto3_client.return_value.unsubscribe.call_count == 2
