# pylint: skip-file

import pytest
from extract_epic import (format_release_date, get_operating_systems, get_genres, listing_is_game,
                          get_listings_from_json, get_features, get_game_url, get_listing_image)


@pytest.mark.parametrize("image_list, expected", [
    ([{"type": "Thumbnail", "url": "https://example.com/image1.jpg"}, {"type": "Cover", "url": "https://example.com/image2.jpg"}],
     "https://example.com/image1.jpg"),
    ([{"type": "Cover", "url": "https://example.com/image2.jpg"}, {"type": "Thumbnail", "url": "https://example.com/image3.jpg"}],
     "https://example.com/image3.jpg"),
    ([{"type": "Cover", "url": "https://example.com/image2.jpg"}],
     ""),
    ([{"type": "Thumbnail", "url": ""}],
     ""),
    ([], "")
])
def test_get_listing_image(image_list, expected):
    assert get_listing_image(image_list) == expected


@pytest.mark.parametrize("mappings, expected", [
    ([{"pageSlug": "awesome-game"}],
     "https://store.epicgames.com/en-US/p/awesome-game"),
    ([{"pageSlug": "cool-game"}],
     "https://store.epicgames.com/en-US/p/cool-game"),
    ([{"pageSlug": "game-with-dashes"}],
     "https://store.epicgames.com/en-US/p/game-with-dashes"),
])
def test_get_game_url(mappings, expected):
    assert get_game_url(mappings) == expected


@pytest.mark.parametrize("tags, expected", [
    ([{"name": "Multiplayer", "groupName": "feature"}, {"name": "Co-op", "groupName": "feature"}],
     ["Multiplayer", "Co-op"]),
    ([{"name": "Single Player", "groupName": "feature"}, {"name": "RPG", "groupName": "genre"}],
     ["Single Player"]),
    ([{"name": "Strategy", "groupName": "genre"}, {"name": "Action", "groupName": "genre"}],
     []),
    ([{"name": "Cross-Platform", "groupName": "feature"}],
     ["Cross-Platform"]),
    ([], [])
])
def test_get_features(tags, expected):
    assert get_features(tags) == expected


@pytest.mark.parametrize("json_str, expected", [
    ('{"Catalog": {"searchStore": {"elements": [{"id": 1, "name": "Game 1"}, {"id": 2, "name": "Game 2"}]}}}',
     [{"id": 1, "name": "Game 1"}, {"id": 2, "name": "Game 2"}]),
    ('{"Catalog": {"searchStore": {"elements": []}}}', []),
    ('{"Catalog": {"searchStore": {"elements": [{"id": 3, "name": "Game 3"}]}}}',
     [{"id": 3, "name": "Game 3"}]),
    ('{"Catalog": {"searchStore": {"elements": null}}}', None),
])
def test_get_listings_from_json(json_str, expected):
    assert get_listings_from_json(json_str) == expected


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
