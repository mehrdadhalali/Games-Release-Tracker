# pylint: skip-file

import pytest
from extract_epic import format_release_date, get_operating_systems, get_genres


@pytest.mark.parametrize("input_date, expected_output", [
    ("2023-10-10T14:48:00Z", "10/10/23"),
    ("2020-02-29T00:00:00Z", "29/02/20"),
    ("1999-12-31T23:59:59Z", "31/12/99"),
    ("2000-01-01T00:00:00Z", "01/01/00"),
    ("2024-04-01T12:00:00Z", "01/04/24"),
    ("2023-10-10T14:48:00+00:00", "10/10/23"),
    ("2021-05-01T08:30:00-03:00", "01/05/21"),
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
