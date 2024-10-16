# pylint: skip-file

import pytest
from unittest.mock import patch, MagicMock
from extract_epic import format_release_date, get_operating_systems, get_genres, listing_is_game, process_listings
from gql.transport.exceptions import TransportQueryError


@pytest.mark.parametrize("input_date, expected_output", [
    ("2023-10-10T14:48:00Z", "10/10/2023"),
    ("2020-02-29T00:00:00Z", "29/02/2020"),
    ("1999-12-31T23:59:59Z", "31/12/1999"),
    ("2000-01-01T00:00:00Z", "01/01/2000"),
    ("2024-04-01T12:00:00Z", "01/04/2024"),
    ("2023-10-10T14:48:00+00:00", "10/10/2023"),
    ("2021-05-01T08:30:00-03:00", "01/05/2021"),
])
def test_format_release_date(input_date, expected_output):
    assert format_release_date(input_date) == expected_output


@pytest.mark.parametrize("input_tags, expected_output", [
    ([{"name": "Windows", "groupName": "platform"},
      {"name": "Linux", "groupName": "platform"},
      {"name": "MacOS", "groupName": "platform"}], ["Windows", "Linux", "MacOS"]),
    ([{"name": "Windows", "groupName": "platform"},
      {"name": "Ubuntu", "groupName": "Linux"},
      {"name": "MacOS", "groupName": "platform"},
      {"name": "iOS", "groupName": "platform"}], ["Windows", "MacOS", "iOS"]),
    ([{"name": "Ubuntu", "groupName": "Linux"},
      {"name": "iOS", "groupName": "mobile"}], []),
    ([], []),
    ([{"name": "Windows"}, {"name": "Linux"}, {
     "name": "MacOS"}], []),
    ([{"name": "Windows", "groupName": "platform"}, {"details": {
     "name": "Linux", "groupName": "platform"}}], ["Windows"]),
])
def test_get_operating_systems(input_tags, expected_output):
    assert get_operating_systems(input_tags) == expected_output


@pytest.mark.parametrize("input_tags, expected_output", [
    ([{"name": "Action", "groupName": "genre"},
      {"name": "Adventure", "groupName": "genre"},
      {"name": "Comedy", "groupName": "genre"}], ["Action", "Adventure", "Comedy"]),
    ([{"name": "Action", "groupName": "genre"},
      {"name": "Thriller", "groupName": "suspense"},
      {"name": "Horror", "groupName": "genre"},
      {"name": "Drama", "groupName": "genre"}], ["Action", "Horror", "Drama"]),
    ([{"name": "Pop", "groupName": "music"},
      {"name": "Rock", "groupName": "music"}], []),
    ([], []),
    ([{"name": "Action"}, {"name": "Drama"}, {"name": "Comedy"}], []),
    ([{"name": "Rock", "groupName": "music"}, {
     "name": "Jazz", "groupName": "genre"}], ["Jazz"]),
])
def test_get_genres(input_tags, expected_output):
    assert get_genres(input_tags) == expected_output


@pytest.mark.parametrize("input_categories, expected_output", [
    ([{"path": "games/action/adventure"}], True),
    ([{"path": "games/roleplaying"}], True),
    ([{"path": "games/simulation"}], True),
    ([{"path": "games/addons/expansion"}], False),
    ([{"path": "games/digitalextras"}], False),
    ([{"path": "games/spthidden"}], False),
    ([{"path": "games/indie"}], True),
    ([{"path": "games/arcade"}], True),
    ([{"path": "games/addons"}, {"path": "games/digitalextras"}], False),
    ([{"path": "games/addons"}, {"path": "games/soundtracks"}], False),
    ([], True),
])
def test_listing_is_game(input_categories, expected_output):
    assert listing_is_game(input_categories) == expected_output


def test_process_listings_unavailable_api():
    """Tests that when the API is not available, a reasonable response is still returned from the lambda."""
    with patch('extract_epic.execute_query') as fake_execute:
        fake_execute.side_effect = TransportQueryError("Unavailable API.")
        listings = process_listings()
        needed_keys = ["platform", "listings"]
        assert all([key in listings for key in needed_keys])
        assert isinstance(listings['listings'], list)
