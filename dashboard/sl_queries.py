"""
This script includes dashboard functions and queries to the database.
"""

from os import environ as ENV
from datetime import datetime

from psycopg2 import connect
import altair as alt
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    '''Returns a connection to the RDS database'''
    return connect(host=ENV["DB_HOST"],
                   port=ENV["DB_PORT"],
                   user=ENV["DB_USER"],
                   password=ENV["DB_PASSWORD"],
                   database=ENV["DB_NAME"])

# Releases table


def get_game_data(show_nsfw):
    '''
    Retrieves game information for the dashboard table including
    name, genres, release date, platform, price, and listing URL.
    '''
    # Adjust the query based on the NSFW filter
    query = """
    SELECT
        g.game_title AS game_name,
        STRING_AGG(DISTINCT ge.genre_name, ', ') AS game_genres,
        CAST(g.release_date AS DATE) AS release_date,
        p.platform_name AS platform,
        gl.release_price,
        gl.listing_url
    FROM game g
    LEFT JOIN game_genre_assignment ga ON g.game_id = ga.game_id
    LEFT JOIN genre ge ON ga.genre_id = ge.genre_id
    LEFT JOIN game_listing gl ON g.game_id = gl.game_id
    LEFT JOIN platform p ON gl.platform_id = p.platform_id
    WHERE (%s OR g.is_nsfw = FALSE)
    GROUP BY g.game_title, g.release_date, p.platform_name, gl.release_price, gl.listing_url
    ORDER BY g.release_date DESC;
    """

    conn = get_connection()
    df = pd.read_sql(query, conn, params=(show_nsfw,)) # Checkbox result
    conn.close()

    return df


# All time stats

def get_weekdays_data():  # Donut chart
    '''Retrieves release dates from the database'''
    query = "SELECT release_date FROM game;"
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df


def get_daily_game_count():  # Line chart
    '''Retrieves the count of distinct game titles for each release date.'''
    query = """
    SELECT
        g.release_date::date AS release_date,
        COUNT(DISTINCT g.game_title) AS total_games
    FROM game g
    GROUP BY g.release_date
    ORDER BY g.release_date;
    """
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df
