"""This script includes functions used in the dashboard."""

import re
from collections import Counter
import numpy as np

import streamlit as st
import pandas as pd
import altair as alt
from nltk.corpus import stopwords as nltk_stopwords
from nltk.tokenize import word_tokenize
from wordcloud import WordCloud
import matplotlib.pyplot as plt

from sl_queries import get_game_data, get_weekdays_data, get_daily_game_count, get_daily_releases, get_genre_data

COLOURS = ['#6a0dad', '#A26ED5', '#3b5998',
           '#5780d9', '#a80dad', '#e426eb', '#0539f7']


def create_donut_chart():
    """Creates a donut chart about weekday releases."""
    release_data = get_weekdays_data()
    release_data['release_date'] = pd.to_datetime(
        release_data['release_date'])  # Convert
    release_data['day_of_week'] = release_data['release_date'].dt.day_name()

    day_counts = release_data['day_of_week'].value_counts().reset_index()
    day_counts.columns = ['Weekday', 'Count']

    total_counts = day_counts['Count'].sum()
    day_counts['Percentage'] = (
        day_counts['Count'] / total_counts) * 100  # Percentages

    donut_chart = alt.Chart(day_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field='Percentage', type='quantitative'),
        color=alt.Color(field='Weekday', type='nominal', scale=alt.Scale(
            domain=day_counts['Weekday'].tolist(), range=COLOURS)),
        tooltip=[
            'Weekday',
            alt.Tooltip('Percentage:Q', format=".2f")
        ]
    ).properties(
        title=alt.TitleParams(
            text='Distribution of Game Releases by Weekday',
            anchor='end',
            fontSize=16
        )
    )

    return donut_chart


def create_line_chart():
    daily_game_data = get_daily_game_count()
    daily_game_data['release_date'] = pd.to_datetime(
        daily_game_data['release_date'])

    line_chart = alt.Chart(daily_game_data).mark_line(color=COLOURS[0], point=True).encode(
        x=alt.X('release_date:T', title='Release Date',
                axis=alt.Axis(format='%Y-%m-%d')),
        y=alt.Y('total_games:Q', title='Total Games'),
        tooltip=['release_date:T', 'total_games:Q']
    ).properties(
        title=alt.TitleParams(
            text='Daily Count of Unique Game Releases',
            anchor='middle',
            fontSize=17
        )
    )

    return line_chart


def create_platform_bar_chart(os_selection, start_date, end_date, show_nsfw):
    """Chart for the number of games released on each platform."""
    game_data = get_game_data(show_nsfw, start_date, end_date, os_selection)

    # Count the number of games per platform
    platform_counts = game_data['platform'].value_counts().reset_index()
    platform_counts.columns = ['Platform', 'Game Count']

    # Create the bar chart
    bar_chart = alt.Chart(platform_counts).mark_bar(color=COLOURS[0]).encode(
        x=alt.X('Platform:N', title='Gaming Platform',
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Game Count:Q', title='Number of Games'),
        tooltip=['Platform:N', 'Game Count:Q']
    ).properties(
        title=alt.TitleParams(
            text='Game Releases per Platform',
            anchor='middle',
            fontSize=17
        )
    )

    return bar_chart


def create_os_bar_chart(show_nsfw, os_selection, start_date, end_date):
    """Bar chart for releases per operating system."""
    # Get the game data based on the selected filters
    game_data = get_game_data(show_nsfw, start_date, end_date, os_selection)

    # Split the 'os_name' column into individual operating systems
    game_data['os_name'] = game_data['os_name'].str.split(', ')

    # Flatten the DataFrame so that each OS has its own row
    game_data = game_data.explode('os_name')

    # Count the number of games per operating system
    os_counts = game_data['os_name'].value_counts().reset_index()
    os_counts.columns = ['Operating System', 'Game Count']

    os_bar_chart = alt.Chart(os_counts).mark_bar(color=COLOURS[0]).encode(
        x=alt.X('Operating System:N', title='Operating System',
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Game Count:Q', title='Number of Games'),
        tooltip=['Operating System:N', 'Game Count:Q']
    ).properties(
        title=alt.TitleParams(
            text='Game Releases by Operating System',
            anchor='middle',
            fontSize=17
        )
    )

    return os_bar_chart


def create_release_line_chart(show_nsfw, start_date, end_date):
    """Line chart for platform releases over time."""
    daily_data = get_daily_releases(show_nsfw, start_date, end_date)

    # Check if start and end date are the same
    if start_date == end_date:
        return None  # Do not display the chart if the dates are the same

    # Count the number of releases per day per platform
    daily_counts = daily_data.groupby(
        ['release_date', 'platform_name']).size().reset_index(name='release_count')

    # Create the line chart
    line_chart = alt.Chart(daily_counts).mark_line(point=True).encode(
        x=alt.X('release_date:T', title='Release Date'),
        y=alt.Y('release_count:Q', title='Number of Releases'),
        color=alt.Color('platform_name:N', scale=alt.Scale(
            domain=['Epic', 'GOG', 'Steam'], range=[COLOURS[1], COLOURS[0], COLOURS[3]]),
            title='Platform'),
        tooltip=['release_date:T', 'release_count:Q', 'platform_name:N']
    ).properties(
        title=alt.TitleParams(
            text='Daily Game Releases Across Platforms',
            anchor='middle',
            fontSize=17
        )
    )

    return line_chart


def create_genre_bar_chart(show_nsfw, start_date, end_date):
    """Creates a horizontal bar chart for genre popularity."""
    genre_data = get_genre_data(show_nsfw, start_date, end_date)

    genre_bar_graph = alt.Chart(genre_data).mark_bar(color=COLOURS[0]).encode(
        # Sort by x in descending order
        y=alt.Y('genre_name:N', title='Genre', sort='-x'),
        x=alt.X('game_count:Q', title='Number of Games'),
        tooltip=['genre_name:N', 'game_count:Q']
    ).properties(
        title=alt.TitleParams(
            text='Most Popular Game Genres',
            anchor='middle',
            fontSize=17
        )
    )

    return genre_bar_graph


def preprocess_descriptions(descriptions):
    """
    Preprocess game descriptions: lowercasing, removing punctuation, filtering stopwords.
    """
    stop_words = set(nltk_stopwords.words('english'))

    cleaned_words = []
    for desc in descriptions:
        # Remove punctuation and tokenize words
        words = word_tokenize(re.sub(r'[^\w\s]', '', desc.lower()))
        # Filter out stop words and words shorter than 3 characters
        words = [
            word for word in words if word != "game" and word not in stop_words and len(word) > 2]
        cleaned_words.extend(words)

    word_counts = Counter(cleaned_words)

    return dict(word_counts)


def create_word_cloud(word_counts):
    """
    Create a word cloud from the provided word counts.
    """
    word_cloud = WordCloud(
        width=1000,
        height=400,
        background_color="#1e1e1e",
        colormap="Purples",
        max_words=40,
        margin=0
    ).generate_from_frequencies(dict(word_counts))

    # Plot the word cloud
    fig, ax = plt.subplots()
    ax.imshow(word_cloud, interpolation='bilinear')
    ax.axis('off')
    plt.tight_layout(pad=0)

    return fig
