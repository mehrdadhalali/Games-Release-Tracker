"""This is the test file for sl_queries.py."""
# pylint: skip-file

from unittest.mock import patch, MagicMock

import pytest
import pandas as pd
from dotenv import load_dotenv

from sl_queries import (
    get_connection,
    get_game_data,
    get_daily_releases,
    get_weekdays_data,
    get_daily_game_count,
    get_genre_data,
    get_game_descriptions,
)

load_dotenv()

# Mock data
mock_game_data = pd.DataFrame({
    'game_name': ['Game 1', 'Game 2'],
    'game_genres': ['Action, Adventure', 'Puzzle'],
    'release_date': ['2023-01-01', '2023-02-01'],
    'platform': ['Steam', 'Epic Games'],
    'release_price': [1999, 1499],
    'listing_url': ['http://game1.com', 'http://game2.com'],
    'os_name': ['Windows, Mac', 'Windows']
})

mock_daily_releases_data = pd.DataFrame({
    'release_date': ['2023-01-01', '2023-02-01'],
    'platform_name': ['Steam', 'Epic Games']
})

mock_genre_data = pd.DataFrame({
    'genre_name': ['Action', 'Adventure'],
    'game_count': [5, 3]
})

mock_descriptions = ['Description 1', 'Description 2']


@pytest.fixture(scope='module')
def db_connection():
    """Fixture to provide a database connection."""
    conn = get_connection()
    yield conn
    conn.close()


@patch('sl_queries.get_connection')
def test_get_weekdays_data(mock_get_connection):
    """Test retrieval of weekdays data."""
    mock_cursor = MagicMock()
    # Assuming you would have expected mock data for weekdays data
    mock_cursor.fetchall.return_value = [('2023-01-01',), ('2023-01-02',)]
    mock_get_connection.return_value.cursor.return_value = mock_cursor

    result = get_weekdays_data()
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert 'release_date' in result.columns


@patch('sl_queries.get_connection')
def test_get_daily_game_count(mock_get_connection):
    """Test retrieval of daily game counts."""
    mock_cursor = MagicMock()
    # Assuming you would have expected mock data for daily game count
    mock_cursor.fetchall.return_value = [('2023-01-01', 1), ('2023-01-02', 2)]
    mock_get_connection.return_value.cursor.return_value = mock_cursor

    result = get_daily_game_count()
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert 'release_date' in result.columns
    assert 'total_games' in result.columns


@patch('sl_queries.get_connection')
def test_get_game_data(mock_get_connection):
    """Test retrieval of game data."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = mock_game_data.values.tolist()
    mock_get_connection.return_value.cursor.return_value = mock_cursor

    result = get_game_data(show_nsfw=True, start_date='2020-01-01',
                           end_date='2024-01-01', os_selection='-All-')
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert 'game_name' in result.columns
    assert result['game_name'].iloc[0] == 'Game 1'


@patch('sl_queries.get_connection')
def test_get_daily_releases(mock_get_connection):
    """Test retrieval of daily releases."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = mock_daily_releases_data.values.tolist()
    mock_get_connection.return_value.cursor.return_value = mock_cursor

    result = get_daily_releases(
        show_nsfw=True, start_date='2020-01-01', end_date='2024-01-01')
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert 'release_date' in result.columns


@patch('sl_queries.get_connection')
def test_get_genre_data(mock_get_connection):
    """Test retrieval of genre data."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = mock_genre_data.values.tolist()
    mock_get_connection.return_value.cursor.return_value = mock_cursor

    result = get_genre_data(
        show_nsfw=True, start_date='2020-01-01', end_date='2024-01-01')
    assert isinstance(result, pd.DataFrame)
    assert not result.empty
    assert 'genre_name' in result.columns


@patch('sl_queries.get_connection')
def test_get_game_descriptions(mock_get_connection):
    """Test retrieval of game descriptions."""
    mock_cursor = MagicMock()
    mock_cursor.fetchall.return_value = [(desc,) for desc in mock_descriptions]
    mock_get_connection.return_value.cursor.return_value = mock_cursor

    result = get_game_descriptions(
        show_nsfw=True, start_date='2020-01-01', end_date='2024-01-01', os_selection='-All-')
    assert isinstance(result, list)
    assert len(result) > 0
    assert result[0] == 'Description 1'
