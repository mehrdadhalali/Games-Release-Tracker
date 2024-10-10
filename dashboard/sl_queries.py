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
def get_game_data():
    '''
    Retrieves game information for the dashboard table including
    name, genres, release date, platform, price, and listing URL.
    '''
    query = """
    SELECT
        g.game_title AS game_name,
        STRING_AGG(DISTINCT ge.genre_name, ', ') AS game_genres,
        g.release_date,
        p.platform_name AS platform,
        gl.release_price,
        gl.listing_url
    FROM game g
    LEFT JOIN game_genre_assignment ga ON g.game_id = ga.game_id
    LEFT JOIN genre ge ON ga.genre_id = ge.genre_id
    LEFT JOIN game_listing gl ON g.game_id = gl.game_id
    LEFT JOIN platform p ON gl.platform_id = p.platform_id
    GROUP BY g.game_title, g.release_date, p.platform_name, gl.release_price, gl.listing_url  -- Include listing URL in the GROUP BY clause
    ORDER BY g.release_date DESC;
    """
    conn = get_connection()
    df = pd.read_sql(query, conn)
    conn.close()
    return df


# All time stats

