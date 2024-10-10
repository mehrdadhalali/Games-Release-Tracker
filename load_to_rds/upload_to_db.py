"""This script is for uploading the listings to the database."""

from get_data_from_database import get_connection, get_ids
from transform_game_data import transform_to_tuples


def upload_game(game: dict) -> int:
    """Uploads a single game to the game table, returning its id."""

    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute("""INSERT INTO game 
                         (game_title, game_description, release_date, is_NSFW, image_URL)
                         VALUES (%s,%s,%s,%s,%s) RETURNING game_id;""",
                         transform_to_tuples(game))
            conn.commit()
            rows = curs.fetchone()

    return rows


def upload_listing(game: dict, game_id: int, platform: str) -> None:
    """Uploads the listing details to the listing table."""

    platform_to_id = get_ids("platform")
    platform_id = platform_to_id[platform]

    with get_connection() as conn:
        with conn.cursor() as curs:
            curs.execute("""INSERT INTO game_listing 
                         (game_id, platform_id, release_price, listing_url)
                         VALUES (%s,%s,%s,%s);""",
                         (game_id, platform_id, game["current_price"], game["url"]))
            conn.commit()


def upload_listing_to_database(game: dict, platform: str):
    """Updates all of the tables in the database with a single listing."""

    game_id = upload_game(game)["game_id"]
    upload_listing(game=game, game_id=game_id, platform=platform)


if __name__ == "__main__":

    game = {
        "title": "The Supper: New Blood Demo",
        "description": "The Supper: New Blood is coming soon and can be wishlisted \nhere\nThe Supper: New Blood is a hilarious horror adventure game for fans of dark humor, bizarre puzzles, and exquisite food!\nStewie S. Appleton runs the remote Twin Sisters Motel in complete solitude. He has no family, no friends, and no hope for a better future. He has suffered all kinds of humiliation and abuse from a cruel world, but he\u2019s had enough. Inspired by his family\u2019s culinary legacy, he will finally take justice into his own hands.\nDo you hear the doorbell, Stewie? Your first guest is here...and something tells me they\u2019ll never leave this motel...\nFrom Octavi Navarro, creator of the critically acclaimed Midnight Scenes game series, and artist on Thimbleweed Park , comes this crazy horror adventure game for fans of the genre. A guilty pleasure for the most exquisite palate.\n\u00a0Refreshing, macabre, point-and-click horror adventure game.Play as Stewie, a lonely soul who wants to make the world a better place...in his own way.Help Stewie fetch all the ingredients, solve funny and bizarre puzzles, and cook his delicious menu.Investigate what dark secrets your guests hide, and choose your victim!Tasty, colorful pixel art!Eerie original soundtrack and sound effects that will make your skin crawl.And don\u2019t forget to feed Inferno . It\u2019s an orange cat. You know what that means.\n\nThe Twin Sisters Motel opens its doors for you\u2026\n\n\n            \n            \n            The Supper: New Blood \u00a9 2024 Octavi Navarro. All rights reserved.",
        "img_url": "https://images.gog-statics.com/fa83fac318efd4d2c1d54d70a0fba1cc3e1cb0502e5bce96d8fc2e83fbf29007_product_card_v2_mobile_slider_639.jpg",
        "genres": [
            "Adventure",
            "Point-and-click",
            "Puzzle"
        ],
        "tags": [
            "Adventure, ",
            "Story Rich, ",
            "Puzzle, ",
            "Dark, "
        ],
        "operating_systems": [
            "Windows"
        ],
        "current_price": 0,
        "release_date": "07/10/2024",
        "url": "https://www.gog.com/en/game/the_supper_new_blood_demo"
    }
    print(upload_listing_to_database(game, "GOG"))
