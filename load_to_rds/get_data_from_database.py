"""This script is for getting data from the RDS, to help with uploading data in other places."""

from os import environ as ENV
from datetime import datetime

from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import RealDictCursor
from dotenv import load_dotenv

load_dotenv()


def get_connection() -> connection:
    """Returns a live DB connection."""

    return connect(
        host=ENV["DB_HOST"],
        user=ENV["DB_USER"],
        dbname=ENV["DB_NAME"],
        port=ENV["DB_PORT"],
        password=ENV["DB_PASSWORD"],
        cursor_factory=RealDictCursor
    )


def get_ids(table_name: str, conn: connection, column_prefix: str = None) -> dict:
    """Gets a map from a table's element names to their ids."""

    if column_prefix is None:
        column_prefix = table_name

    with conn.cursor() as curs:
        curs.execute(f"""SELECT {column_prefix}_name,
                    {column_prefix}_id FROM {table_name};""")
        rows = curs.fetchall()

    name_to_id = {row[f"{column_prefix}_name"]: row[f"{column_prefix}_id"]
                  for row in rows}

    return name_to_id


def get_listings_for_the_day(day: datetime.date, conn: connection) -> list[str]:
    """Returns a list of listings already scraped that day."""

    with conn.cursor() as curs:
        curs.execute("""SELECT listing_url
                     FROM game_listing
                     JOIN game USING (game_id) 
                     WHERE release_date = %s;""", (day,))
        rows = curs.fetchall()
        return [row["listing_url"]
                for row in rows]


if __name__ == "__main__":

    ...
