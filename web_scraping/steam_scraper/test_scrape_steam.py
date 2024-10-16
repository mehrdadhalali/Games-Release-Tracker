"""Tests for the scrape_steam.py file."""

# pylint: skip-file

from unittest import mock
from bs4 import BeautifulSoup
from datetime import datetime

import pytest

from scrape_steam import (load_page_source, format_price, get_steam_app_url, parse_release_date,
                          scrape_game_description, scrape_game_tags, scrape_game_nsfw, scrape_game_genres,
                          scrape_game_operating_systems)


@pytest.mark.parametrize("html, expected", [
    ('<span class="platform_img win"></span>', ['Windows']),
    ('<span class="platform_img mac"></span>', ['Mac']),
    ('<span class="platform_img linux"></span>', ['Linux']),
    ('<span class="platform_img win"></span><span class="platform_img mac"></span>',
     ['Windows', 'Mac']),
    ('<span class="platform_img win"></span><span class="platform_img linux"></span><span class="platform_img mac"></span>',
     ['Windows', 'Linux', 'Mac']),
    ('<span class="platform_img unknown"></span>', []),
    ('<div class="platform_img"></div>', []),
    ('', [])
])
def test_scrape_game_operating_systems(html, expected):
    soup = BeautifulSoup(html, 'html.parser')
    assert sorted(scrape_game_operating_systems(soup)) == sorted(expected)


@pytest.mark.parametrize("html, expected", [
    ('<div id="genresAndManufacturer"><a href="/genre/action">Action</a><a href="/genre/adventure">Adventure</a></div>',
     ['Action', 'Adventure']),
    ('<div id="genresAndManufacturer"><a href="/genre/rpg">RPG</a><a href="/other">Other</a></div>',
     ['RPG']),
    ('<div id="genresAndManufacturer"><a href="/genre/strategy"> Strategy </a></div>',
     ['Strategy']),
    ('<div id="genresAndManufacturer"></div>', [])
])
def test_scrape_game_genres(html, expected):
    soup = BeautifulSoup(html, 'html.parser')
    assert scrape_game_genres(soup) == expected


@pytest.mark.parametrize("html, expected", [
    ('<h2>Mature Content</h2>', True),
    ('<h2>Contains Mature content</h2>', True),
    ('<h2>Violence</h2><h2>Mature Content</h2>', True),
    ('<h2>Violence</h2><h2>Blood</h2>', False),
    ('<h2></h2>', False),
    ('', False)
])
def test_scrape_game_nsfw(html, expected):
    soup = BeautifulSoup(html, 'html.parser')
    assert scrape_game_nsfw(soup) == expected


@pytest.mark.parametrize("html, expected", [
    ('<a class="app_tag">Singleplayer</a><a class="app_tag">Adventure</a>',
     ['Singleplayer', 'Adventure']),
    ('<a class="app_tag"> RPG </a><a class="app_tag">Strategy</a>',
     ['RPG', 'Strategy']),
    ('<a class="app_tag">Multiplayer</a>', ['Multiplayer']),
    ('<div class="no_tags"></div>', []),
    ('', [])
])
def test_scrape_game_tags(html, expected):
    soup = BeautifulSoup(html, 'html.parser')
    assert scrape_game_tags(soup) == expected


@pytest.mark.parametrize("html, expected", [
    ('<div class="game_description_snippet">This is a great game.</div>',
     'This is a great game.'),
    ('<div class="game_description_snippet"> This is not a great game! </div>',
     'This is not a great game!'),
    ('<div class="game_description_snippet"></div>', ''),
    ('<div></div>', 'No description available.'),
    ('', 'No description available.')
])
def test_scrape_game_description(html, expected):
    """Tests that the scrape game description function can handle a range of inputs."""
    soup = BeautifulSoup(html, 'html.parser')
    assert scrape_game_description(soup) == expected


@pytest.mark.parametrize("html, expected", [
    ('<div class="search_released">13 October, 2020</div>', datetime(2020, 10, 13)),
    ('<div class="search_released">October 2020</div>', datetime(2020, 10, 1)),
    ('<div class="search_released">13 Oct, 2020</div>', datetime(2020, 10, 13)),
    ('<div class="search_released">2020-10-13</div>', datetime(2020, 10, 13)),
    ('<div class="search_released"></div>', None),
    ('<div></div>', None),
    ('', None)
])
def test_parse_release_date(html, expected):
    """Tests that the parse release date is capable of parsing a range of different date strings."""
    soup = BeautifulSoup(html, 'html.parser')
    assert parse_release_date(soup) == expected


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


@pytest.mark.parametrize(
    "app_id, expected_url",
    [
        ("12345", "https://store.steampowered.com/app/12345/"),
        ("67890", "https://store.steampowered.com/app/67890/"),
        ("abcde", "https://store.steampowered.com/app/abcde/"),
        ("", "https://store.steampowered.com/app//"),
    ]
)
def test_get_steam_app_url(app_id, expected_url):
    """Tests that steam app urls are correctly formed."""
    assert get_steam_app_url(app_id) == expected_url
