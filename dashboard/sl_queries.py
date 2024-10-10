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


def get_game_data(show_nsfw, start_date, end_date, os_selection):
    '''
    Retrieves game information for the dashboard table including
    name, genres, release date, platform, price, and listing URL.
    Filters by platform, date range, and operating system if provided.
    '''
    query = """
    SELECT
        g.game_title AS game_name,
        STRING_AGG(DISTINCT ge.genre_name, ', ') AS game_genres,
        CAST(g.release_date AS DATE) AS release_date,
        p.platform_name AS platform,
        gl.release_price,
        gl.listing_url,
        os.os_name
    FROM game g
    LEFT JOIN game_genre_assignment ga ON g.game_id = ga.game_id
    LEFT JOIN genre ge ON ga.genre_id = ge.genre_id
    LEFT JOIN game_listing gl ON g.game_id = gl.game_id
    LEFT JOIN platform p ON gl.platform_id = p.platform_id
    LEFT JOIN game_os_assignment goa ON g.game_id = goa.game_id
    LEFT JOIN operating_system os ON goa.os_id = os.os_id
    WHERE (%s OR g.is_nsfw = FALSE)
    """

    params = [show_nsfw]

    # Add date range filter
    query += " AND g.release_date BETWEEN %s AND %s"
    params.append(start_date)
    params.append(end_date)

    # Add operating system filter if a specific OS is selected
    if os_selection != "-All-":
        query += " AND os.os_name = %s"
        params.append(os_selection)

    query += """
    GROUP BY g.game_title, g.release_date, p.platform_name, gl.release_price, gl.listing_url, os_name
    ORDER BY g.release_date DESC;
    """

    # Execute the query with the parameters
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()

    # Convert the result to a pandas DataFrame
    df = pd.DataFrame(result, columns=[
        'game_name', 'game_genres', 'release_date', 'platform', 'release_price', 'listing_url', 'os_name'
    ])

    df['release_price'] = df['release_price'] / 100  # Convert to pounds

    cursor.close()
    conn.close()

    return df


def get_daily_releases(show_nsfw, start_date, end_date):
    """
    Retrieves the number of games released on each platform between the chosen dates.
    """
    query = """
    SELECT 
        g.release_date,
        p.platform_name
    FROM game g
    LEFT JOIN game_listing gl ON g.game_id = gl.game_id
    LEFT JOIN platform p ON gl.platform_id = p.platform_id
    WHERE (%s OR g.is_nsfw = FALSE)
    AND g.release_date BETWEEN %s AND %s
    """

    params = [show_nsfw, start_date, end_date]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()

    df = pd.DataFrame(result, columns=['release_date', 'platform_name'])

    cursor.close()
    conn.close()

    return df


# All time stats

def get_weekdays_data():
    '''Retrieves release dates from the database'''
    query = "SELECT release_date FROM game;"

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    # Create DataFrame from the fetched result manually
    df = pd.DataFrame(result, columns=['release_date'])

    cursor.close()
    conn.close()
    return df


def get_daily_game_count():
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
    cursor = conn.cursor()
    cursor.execute(query)
    result = cursor.fetchall()

    # Create DataFrame from the fetched result manually
    df = pd.DataFrame(result, columns=['release_date', 'total_games'])

    cursor.close()
    conn.close()
    return df


def get_genre_data(show_nsfw, start_date, end_date):
    """
    Retrieves information about the most frequent genres for releases.
    """
    query = """
    SELECT 
        STRING_AGG(DISTINCT ge.genre_name, ', ') AS genre_name,
        COUNT(g.game_id) AS game_count
    FROM game g
    LEFT JOIN game_genre_assignment ga ON g.game_id = ga.game_id
    LEFT JOIN genre ge ON ga.genre_id = ge.genre_id
    WHERE (%s OR g.is_nsfw = FALSE)
    AND g.release_date BETWEEN %s AND %s
    GROUP BY ge.genre_name LIMIT 10;
    """

    params = [show_nsfw, start_date, end_date]

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(query, params)
    result = cursor.fetchall()

    df = pd.DataFrame(result, columns=['genre_name', 'game_count'])

    cursor.close()
    conn.close()

    return df
