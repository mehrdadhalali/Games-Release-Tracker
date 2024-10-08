"""Tests for the scrape_steam.py file."""
# pylint: skip-file

from unittest import mock

import pytest

from scrape_steam import load_page_source


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
