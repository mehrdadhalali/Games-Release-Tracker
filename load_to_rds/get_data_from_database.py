"""This script is for getting data from the database, to help with uploading data in other places."""

from os import environ as ENV

from psycopg2 import connect
from psycopg2.extensions import connection
from psycopg2.extras import execute_values, RealDictCursor
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


def get_ids(table_name: str, column_prefix: str = None) -> dict:
    """Gets a map from a table's element names to their ids."""

    if column_prefix is None:
        column_prefix = table_name

    conn = get_connection()
    with conn.cursor() as curs:
        curs.execute(f"""SELECT {column_prefix}_name,
                      {column_prefix}_id FROM {table_name};""")
        rows = curs.fetchall()
    conn.close()

    name_to_id = {row[f"{column_prefix}_name"]: row[f"{column_prefix}_id"]
                  for row in rows}

    return name_to_id


if __name__ == "__main__":

    print(get_ids("platform", "platform"))
