"""This is the test file for functions.py."""
# pylint: skip-file

from unittest.mock import patch

import pandas as pd
import altair as alt
import matplotlib.pyplot as plt

from functions import (
    create_donut_chart,
    create_line_chart,
    display_game_table,
    create_platform_bar_chart,
    preprocess_descriptions,
    create_word_cloud
)

# Sample mock data
mock_weekday_data = pd.DataFrame({
    'release_date': ['2023-01-01', '2023-01-02', '2023-01-03'],
    'platform_name': ['Steam', 'Epic', 'Steam']
})

mock_daily_game_count_data = pd.DataFrame({
    'release_date': ['2023-01-01', '2023-01-02'],
    'total_games': [5, 3]
})

mock_game_data = pd.DataFrame({
    'game_name': ['Game 1', 'Game 2'],
    'game_genres': ['Action', 'Adventure'],
    'release_date': ['2023-01-01', '2023-01-02'],
    'platform': ['Steam', 'Epic'],
    'release_price': [1999, 1499],
    'listing_url': ['http://game1.com', 'http://game2.com'],
    'os_name': ['Windows', 'Mac']
})

mock_genre_data = pd.DataFrame({
    'genre_name': ['Action', 'Adventure'],
    'game_count': [5, 3]
})

mock_descriptions = ["A thrilling adventure game.", "A fun puzzle game."]


@patch('functions.get_weekdays_data')
def test_create_donut_chart(mock_get_weekdays_data):
    """Test for create_donut_chart."""
    mock_get_weekdays_data.return_value = mock_weekday_data
    chart = create_donut_chart()

    assert chart is not None
    assert isinstance(chart, alt.Chart)


@patch('functions.get_daily_game_count')
def test_create_line_chart(mock_get_daily_game_count):
    """Test for create_line_chart."""
    mock_get_daily_game_count.return_value = mock_daily_game_count_data
    chart = create_line_chart()

    assert chart is not None
    assert isinstance(chart, alt.Chart)


@patch('functions.get_game_data')
def test_display_game_table(mock_get_game_data):
    """Test for display_game_table."""
    mock_get_game_data.return_value = mock_game_data

    # To test Streamlit, we may want to test the output HTML
    with patch('streamlit.markdown') as mock_markdown:
        display_game_table(show_nsfw=True, os_selection='-All-',
                           start_date='2020-01-01', end_date='2024-01-01', search_query='', sort_by="")
        mock_markdown.assert_called_once()  # Ensure that the markdown function was called


@patch('functions.get_game_data')
def test_create_platform_bar_chart(mock_get_game_data):
    """Test for create_platform_bar_chart."""
    mock_get_game_data.return_value = mock_game_data
    chart = create_platform_bar_chart(
        '-All-', '2020-01-01', '2024-01-01', True)

    assert chart is not None
    assert isinstance(chart, alt.Chart)
