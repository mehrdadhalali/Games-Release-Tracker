"""This script is for uploading the listings to the database."""

from json import load
from datetime import datetime

from psycopg2.extensions import connection
from psycopg2.extras import execute_values

from get_data_from_database import get_connection, get_ids, get_listings_for_the_day
from transform_game_data import transform_to_tuples


def update_genres(new_genres: list[str], conn: connection) -> dict:
    """Adds any new genres to the genre table, returning their id map."""

    query = "INSERT INTO genre (genre_name) VALUES %s RETURNING genre_id, genre_name;"

    with conn.cursor() as curs:
        execute_values(curs, query, new_genres)
        rows = curs.fetchall()
    conn.commit()

    return {row["genre_name"]: row["genre_id"]
            for row in rows}


def upload_game(game: dict, conn: connection) -> int:
    """Uploads a single game to the game table, returning its id."""

    with conn.cursor() as curs:
        curs.execute("""INSERT INTO game
                        (game_title, game_description, release_date, is_NSFW, image_URL)
                        VALUES (%s,%s,%s,%s,%s) RETURNING game_id;""",
                     transform_to_tuples(game))
        conn.commit()
        rows = curs.fetchone()

    return rows


def upload_listing(game: dict, game_id: int, platform: str,
                   platform_to_id: dict, conn: connection) -> None:
    """Uploads the listing details to the listing table."""

    platform_id = platform_to_id[platform]

    with conn.cursor() as curs:
        curs.execute("""INSERT INTO game_listing
                        (game_id, platform_id, release_price, listing_url)
                        VALUES (%s,%s,%s,%s);""",
                     (game_id, platform_id, game["current_price"], game["url"]))
        conn.commit()


def upload_genre(game_id: int, genres: list[str],
                 genre_to_id: dict, conn: connection) -> None:
    """Updates the genre assignment table in the database."""

    new_genres = [(genre, ) for genre in genres
                  if genre not in genre_to_id.keys()]
    if len(new_genres) > 0:

        new_genre_map = update_genres(new_genres, conn)
        genre_to_id.update(new_genre_map)

    upload_tuples = [(game_id, genre_to_id[genre])
                     for genre in genres]
    query = """INSERT INTO game_genre_assignment
                (game_id, genre_id)
                VALUES %s;"""

    with conn.cursor() as curs:
        execute_values(curs, query, upload_tuples)
    conn.commit()


def upload_os(game_id: int, oss: list[str],
              os_to_id: dict, conn: connection) -> None:
    """Updates the OS assignment table in the database."""

    os_to_id = get_ids("operating_system", "os")

    upload_tuples = [(game_id, os_to_id[os])
                     for os in oss]
    query = """INSERT INTO game_os_assignment
                (game_id, os_id)
                VALUES %s;"""

    with conn.cursor() as curs:
        execute_values(curs, query, upload_tuples)
    conn.commit()


def upload_entire_listing_to_database(game: dict, platform: str,
                                      maps: list[dict], conn: connection) -> None:
    """Updates all of the tables in the database with a single listing."""

    genre_to_id = maps["genre"]
    os_to_id = maps["os"]
    platform_to_id = maps["platform"]

    game_id = upload_game(game, conn)["game_id"]
    upload_listing(game, game_id, platform, platform_to_id, conn)
    upload_genre(game_id, game["genres"], genre_to_id, conn)
    upload_os(game_id, game["operating_systems"], os_to_id, conn)


def upload_all_listings_to_database(json_data: dict, maps: list[dict], conn: connection):
    """Upload all listings to the database."""

    platform = json_data["platform"]
    for listing in json_data["listings"]:
        upload_entire_listing_to_database(listing, platform, maps, conn)


def main():
    """The main function"""

    conn = get_connection()
    maps = {
        "genre": get_ids("genre", conn),
        "platform": get_ids("platform", conn),
        "os": get_ids("operating_system", conn,  "os")
    }

    with open("gog_data.json", "r", encoding="UTF-8") as f:
        gog_data = load(f)

    with open("steam_data.json", "r", encoding="UTF-8") as f:
        steam_data = load(f)

    for listing in steam_data["listings"]:
        listing["release_date"] = datetime.strftime(
            datetime.strptime(listing["release_date"], "%d %b %Y"),
            "%d/%m/%Y"
        )

    already_scraped = get_listings_for_the_day(datetime.today(), conn)
    gog_data["listings"] = [game for game in gog_data["listings"]
                            if game["url"] not in already_scraped]
    steam_data["listings"] = [game for game in steam_data["listings"]
                              if game["url"] not in already_scraped]

    upload_all_listings_to_database(gog_data, maps, conn)
    upload_all_listings_to_database(steam_data, maps, conn)

    conn.close()


if __name__ == "__main__":

    main()
