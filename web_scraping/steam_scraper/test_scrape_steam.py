"""Tests for the scrape_steam.py file."""

# pylint: skip-file

from unittest import mock

import pytest

from scrape_steam import load_page_source, format_price


@pytest.mark.parametrize("price_str, expected", [
    ("$12.34", 1234),
    ("£45.67", 4567),
    ("€89.10", 8910),
    ("1234", 123400),
    ("free", 0),
    ("  fReE", 0),
    ("   FREE   ", 0),
    ("$0.00", 0),
    ("£0.99", 99),
    ("10", 1000),
    ("$100", 10000),
])
def test_format_price(price_str, expected):
    """Tests that the format price function returns appropriate ints
    for a range of given values."""
    assert format_price(price_str) == expected


@mock.patch('requests.get')
def test_load_page_source_200_code_returns_string(mocked_get):
    """Tests that a get request with a 200 status code returns a string of the correct value."""
    mocked_response = mock.MagicMock()
    mocked_response.status_code = 200
    mocked_response.text = "<HTML></HTML>"
    mocked_get.return_value = mocked_response
    sample_url = "https://www.url.com"
    content = load_page_source(sample_url)
    assert isinstance(content, str)
    assert content == mocked_response.text


@mock.patch('requests.get')
def test_load_page_source_404_raises_error(mocked_get):
    """Tests that a get request with a 404 status code raises a connection error."""
    mocked_response = mock.MagicMock()
    mocked_response.status_code = 404
    mocked_get.return_value = mocked_response
    sample_url = "https://www.url.com"
    with pytest.raises(ConnectionError):
        load_page_source(sample_url)


@mock.patch('requests.get')
def test_load_page_source_calls_get(mocked_get):
    """Tests that a function call to load page source calls requests.get once."""
    mocked_get.return_value.status_code = 200
    mocked_get.return_value.text = "Sample Page Content"
    sample_url = "https://www.url.com"
    load_page_source(sample_url)
    assert mocked_get.assert_called_once
