"""The main script to handle database connections, and querying for the report 
generation and emailing."""

from os import environ as ENV

from dotenv import load_dotenv
from psycopg2 import connect
from psycopg2.extras import RealDictCursor
from psycopg2.extensions import cursor, connection

load_dotenv()


def get_connection() -> connection:
    """Returns an open connection to the database."""
    return connect(
        database=ENV['DB_NAME'],
        host=ENV['DB_HOST'],
        user=ENV['DB_USER'],
        password=ENV['DB_PASSWORD'],
        port=ENV['DB_PORT']
    )


def get_cursor(conn: connection) -> cursor:
    """Returns a cursor from a database connection."""
    return conn.cursor(cursor_factory=RealDictCursor)


def get_subscriber_info() -> dict:
    """Returns a dictionary mapping subscriber name to subscriber email."""
    select_str = "SELECT sub_name, sub_email FROM subscriber;"
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(select_str)
            results = cur.fetchall()
    return {x['sub_name']: x['sub_email'] for x in results}


def get_top_genres() -> list[str]:
    """Returns a list of the top three genres from the past week."""
    select_str = """SELECT gr.genre_name, COUNT(*) AS genre_count
    FROM genre AS gr JOIN game_genre_assignment AS gga 
    ON gga.genre_id = gr.genre_id JOIN game AS g 
    ON g.game_id = gga.game_id WHERE g.release_date > 
    CURRENT_TIMESTAMP - INTERVAL '7 days' GROUP BY gr.genre_name
    ORDER BY genre_count DESC LIMIT 3;"""
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute(select_str)
            results = cur.fetchall()
    return [x['genre_name'] for x in results]


def get_all_genres() -> list[str]:
    """Returns a list of all genres in the database."""
    with get_connection() as conn:
        with get_cursor(conn) as cur:
            cur.execute("SELECT * FROM genre;")
            results = cur.fetchall()

    return [x['genre_name'] for x in results]
