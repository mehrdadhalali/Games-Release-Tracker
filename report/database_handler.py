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
