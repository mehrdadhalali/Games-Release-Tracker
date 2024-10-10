# pylint: disable=C0103
"""
This is the main dashboard for the Games Tracker Streamlit application.
It includes data visualisations on the information collected from Steam, GOG and Epic,
which is stored in an AWS RDS database.
"""
from datetime import datetime

import streamlit as st
import pandas as pd
import altair as alt

from sl_queries import get_game_data, get_weekdays_data, get_daily_game_count, get_daily_releases

# Page configuration
st.set_page_config(layout="wide")
COLOURS = ['#6a0dad', '#A26ED5', '#3b5998',
           '#5780d9', '#a80dad', '#e426eb', '#0539f7']

# Function to create the donut chart


def create_donut_chart():
    release_data = get_weekdays_data()
    release_data['release_date'] = pd.to_datetime(
        release_data['release_date'])  # Convert
    release_data['day_of_week'] = release_data['release_date'].dt.day_name()

    day_counts = release_data['day_of_week'].value_counts().reset_index()
    day_counts.columns = ['Day of Week', 'Count']

    total_counts = day_counts['Count'].sum()
    day_counts['Percentage'] = (
        day_counts['Count'] / total_counts) * 100  # Percentages

    donut_chart = alt.Chart(day_counts).mark_arc(innerRadius=50).encode(
        theta=alt.Theta(field='Percentage', type='quantitative'),
        color=alt.Color(field='Day of Week', type='nominal', scale=alt.Scale(
            domain=day_counts['Day of Week'].tolist(), range=COLOURS)),
        tooltip=[
            'Day of Week',
            alt.Tooltip('Percentage:Q', format=".2f")
        ]
    ).properties(
        title='Game Releases by Day of the Week'
    )
    return donut_chart

# Function to create the line chart


def create_line_chart():
    daily_game_data = get_daily_game_count()
    daily_game_data['release_date'] = pd.to_datetime(
        daily_game_data['release_date'])

    line_chart = alt.Chart(daily_game_data).mark_line(point=True).encode(
        x=alt.X('release_date:T', title='Release Date',
                axis=alt.Axis(format='%Y-%m-%d')),
        y=alt.Y('total_games:Q', title='Total Games'),
        tooltip=['release_date:T', 'total_games:Q']
    ).properties(
        title='Daily Distinct Game Releases'
    )
    return line_chart


def display_game_table(show_nsfw, os_selection, start_date, end_date):
    table_data = get_game_data(
        show_nsfw, start_date, end_date, os_selection)

    table_data.drop('os_name', axis=1, inplace=True)
    # Rename columns to make them more readable
    table_data = table_data.rename(
        columns={
            'game_name': 'Title',
            'game_genres': 'Genres',
            'release_date': 'Release Date',
            'platform': 'Platform',
            'release_price': 'Price',
            'listing_url': 'Listing URL'  # Ensure listing_url is included for hyperlinks
        }
    )

    # Convert price from pennies to pounds and format it
    table_data['Price'] = table_data['Price'].apply(lambda x: f"£{x:.2f}")

    # Display the DataFrame with clickable URLs
    st.dataframe(
        table_data,
        column_config={
            "Listing URL": st.column_config.LinkColumn()  # Make the Listing URL clickable
        },
        use_container_width=True
    )


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
        title='Number of Games Released by Platform'
    )
    return bar_chart


def create_os_bar_chart(os_selection, start_date, end_date):
    # Always show NSFW, so set it to True
    show_nsfw = True

    # Get the game data based on the selected filters
    game_data = get_game_data(show_nsfw, start_date, end_date, os_selection)

    # Count the number of games per operating system
    os_counts = game_data['os_name'].value_counts().reset_index()
    os_counts.columns = ['Operating System', 'Game Count']

    # Create the bar chart
    os_bar_chart = alt.Chart(os_counts).mark_bar(color=COLOURS[2]).encode(
        x=alt.X('Operating System:N', title='Operating System',
                axis=alt.Axis(labelAngle=0)),
        y=alt.Y('Game Count:Q', title='Number of Games'),
        tooltip=['Operating System:N', 'Game Count:Q']
    ).properties(
        title='Number of Games Released by Operating System'
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
            domain=['Epic', 'GOG', 'Steam'], range=[COLOURS[1], COLOURS[4], COLOURS[3]])),
        tooltip=['release_date:T', 'release_count:Q', 'platform_name:N']
    ).properties(
        title='Daily Game Releases by Platform',
        width=800,
        height=400
    )

    return line_chart



if __name__ == "__main__":
    # User input for OS selection, date range, and NSFW checkbox
    cols = st.columns([2, 0.75, 1, 0.35])
    with cols[0]:
        st.title("Games Tracker")
    with cols[1]:
        os_selection = st.selectbox(
            "Operating System:",
            options=["-All-", "Windows", "Mac", "Linux"]
        )
    with cols[2]:
        today = datetime.now().date()
        min_date = datetime(2024, 10, 7).date()
        date_range = st.date_input(
            "Select date range:",
            value=[min_date, today],
            min_value=min_date,
            max_value=today,
            format="YYYY-MM-DD"
        )
        start_date, end_date = date_range if len(
            date_range) == 2 else (None, None)
    with cols[3]:
        st.write(" <br> ", unsafe_allow_html=True)
        show_nsfw = st.checkbox("NSFW")

    st.markdown("<small style='color: #A26ED5;'>* The full list of released games is available at the bottom of this dashboard.</small>",
                unsafe_allow_html=True)
    
    # Changing stats
    cols = st.columns(2)
    with cols[0]:
        st.altair_chart(create_platform_bar_chart(os_selection, start_date, end_date, show_nsfw), use_container_width=True)
    with cols[1]:
        st.altair_chart(create_os_bar_chart(
            os_selection, start_date, end_date), use_container_width=True)
        
    st.altair_chart(create_release_line_chart(show_nsfw, start_date, end_date))


    # All time stats
    st.subheader("All Time Stats")
    st.markdown(
        "<style>.line { border: 0.5px solid; margin: 0; }</style><div class='line'></div>", unsafe_allow_html=True)

    cols = st.columns(2)
    with cols[0]:
        st.altair_chart(create_donut_chart(), use_container_width=True)
    with cols[1]:
        st.altair_chart(create_line_chart(), use_container_width=True)

    st.subheader("List of Games")
    st.markdown(
        "<style>.line { border: 0.5px solid; margin: 0; }</style><div class='line'></div>", unsafe_allow_html=True)

    # Game releases table
    display_game_table(show_nsfw, os_selection, start_date, end_date)
