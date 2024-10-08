# pylint: skip-file

from datetime import datetime

import pytest

from upload_to_db import remove_duplicates
from transform_game_data import has_nsfw_tags, transform_to_tuples


def test_remove_duplicates():

    scraped_games = [
        {
            "platform": "Steam",
            "listings":
            [{"url": "url_1"},
             {"url": "url_2"}]
        },
        {
            "platform": "gog",
            "listings":
            [{"url": "url_3"},
             {"url": "yes"}]
        }
    ]
    already_scraped = ["url_1", "url_2", "yes"]

    scraped_games = remove_duplicates(scraped_games, already_scraped)

    assert len(scraped_games[0]["listings"]) == 0
    assert len(scraped_games[1]["listings"]) == 1
    assert scraped_games[1]["listings"][0]["url"] == "url_3"


@pytest.mark.parametrize("game,is_nsfw",
                         [({"tags": ["Hentai", "Action"]}, True),
                          ({"tags": ["Action", "Blood"]}, False),
                          ({"tags": []}, False),
                          ({"tags": ["nSfW"]}, True)])
def test_has_nsfw_tags(game, is_nsfw):

    assert has_nsfw_tags(game) == is_nsfw


def test_transform_to_tuples():

    game = {
        "title": "Game",
        "description": "something",
        "release_date": "18/09/2020",
        "tags": ["RPG", "Adult content"],
        "img_url": "example.com"
    }

    assert transform_to_tuples(game) == ("Game",
                                         "something",
                                         datetime(2020, 9, 18),
                                         True,
                                         "example.com")
