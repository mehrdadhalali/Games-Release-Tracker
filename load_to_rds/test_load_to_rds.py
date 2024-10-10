# pylint: skip-file

from upload_to_db import remove_duplicates


def test_remove_duplicates():

    scraped_games = [
        {
            "platform": "Steam"
        }
    ]
