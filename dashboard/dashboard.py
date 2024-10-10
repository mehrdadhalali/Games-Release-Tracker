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

from sl_queries import get_game_data, get_weekdays_data, get_daily_game_count

# Page configuration
st.set_page_config(layout="wide")
bright_purple = '#A26ED5'

cols = st.columns([2, 0.75, 1, 0.35])
with cols[0]:
    st.title("Games Tracker")

# Create a dropdown selection
with cols[1]:
    platform_selection = st.selectbox(
        "Operating System:",
        options=["-All-", "Windows", "Mac", "Linux"])

with cols[2]:
    # Get today's date to set as the maximum selectable date
    today = datetime.now().date()

    # Set a specific minimum date (e.g., October 7, 2024)
    min_date = datetime(2024, 10, 7).date()

    # Create a date range selector with "All time" as the default range
    # Default to the range from min_date to today
    default_start_date = min_date
    default_end_date = today

    # Create the date input and store the output
    date_range = st.date_input(
        "Select date range:",
        value=[default_start_date, default_end_date],  # Default range
        min_value=min_date,  # Minimum selectable date
        max_value=today,  # Exclude future dates
        format="YYYY-MM-DD"
    )

    # Check if date_range has two dates to unpack
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        st.warning("Please select both start and end dates.")

with cols[3]:
    st.write(" <br> ", unsafe_allow_html=True)
    show_nsfw = st.checkbox("NSFW")


# All time stats
# Donut Chart
release_data = get_weekdays_data()

release_data['release_date'] = pd.to_datetime(release_data['release_date'])  # Convert
release_data['day_of_week'] = release_data['release_date'].dt.day_name()

day_counts = release_data['day_of_week'].value_counts().reset_index()
day_counts.columns = ['Day of Week', 'Count']

total_counts = day_counts['Count'].sum()
day_counts['Percentage'] = (day_counts['Count'] / total_counts) * 100  # Percentages

donut_chart = alt.Chart(day_counts).mark_arc(innerRadius=50).encode(
    theta=alt.Theta(field='Percentage', type='quantitative'),
    color=alt.Color(field='Day of Week', type='nominal'),
    tooltip=[
        'Day of Week',
        alt.Tooltip('Percentage:Q', format=".2f")
    ]
).properties(
    title=alt.TitleParams(text='Game Releases by Day of the Week',
                          color=bright_purple)
)

#Line Chart
daily_game_data = get_daily_game_count()

daily_game_data['release_date'] = pd.to_datetime(
    daily_game_data['release_date'])

line_chart = alt.Chart(daily_game_data).mark_line(point=True).encode(
    x=alt.X('release_date:T', title='Release Date',
            axis=alt.Axis(format='%Y-%m-%d')),
    y=alt.Y('total_games:Q', title='Total Games'),
    tooltip=['release_date:T', 'total_games:Q']
).properties(
    title=alt.TitleParams(text='Daily Distinct Game Releases',
                          color=bright_purple)
)

st.subheader("All Time Stats")
st.markdown(
    "<style>.line { border: 0.5px solid; margin: 0; }</style><div class='line'></div>", unsafe_allow_html=True)
cols = st.columns(2)
with cols[0]:
    st.altair_chart(donut_chart, use_container_width=True)
with cols[1]:
    st.altair_chart(line_chart, use_container_width=True)


st.subheader("List of Games")
st.markdown(
    "<style>.line { border: 0.5px solid; margin: 0; }</style><div class='line'></div>", unsafe_allow_html=True)

# Game releases table
table_data = get_game_data(show_nsfw)

# Drop the index and rename columns to make them more readable
table_data = table_data.reset_index(drop=True).rename(
    columns={
        'game_name': 'Title',
        'game_genres': 'Genres',
        'release_date': 'Release Date',
        'platform': 'Platform',
        'release_price': 'Price',
        'listing_url': 'Listing URL'  # Ensure listing_url is included for hyperlinks
    }
)

# Convert price from pennies to pounds
table_data['Price'] = (table_data['Price'] / 100).round(2)

# Now use st.dataframe with column_config
st.dataframe(
    table_data,
    column_config={
        "Listing URL": st.column_config.LinkColumn()  # Make the Listing URL clickable
    },
    use_container_width=True
)
