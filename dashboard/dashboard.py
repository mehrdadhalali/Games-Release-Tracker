# pylint: disable=C0103
"""
This is the main dashboard for the Games Tracker Streamlit application.
It includes data visualisations on the information collected from Steam, GOG and Epic,
which is stored in an AWS RDS database.
"""
from datetime import datetime

import streamlit as st

from sl_queries import get_game_data

# Page configuration
st.set_page_config(layout="wide")

cols = st.columns([2, 0.75, 1, 0.4])
with cols[0]:
    st.title("Games Tracker")

# Create a dropdown selection
with cols[1]:
    platform_selection = st.selectbox(
        "Select a platform:",
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

# # Game releases table
# table_data = get_game_data()
# # Drop the index and rename columns to make them more readable
# table_data = table_data.reset_index(drop=True).rename(
#     columns={
#         'game_name': 'Title',
#         'game_genres': 'Genres',
#         'release_date': 'Release Date',
#         'platform': 'Platform',
#         'release_price': 'Price'
#     })
# st.dataframe(table_data)

# Game releases table
table_data = get_game_data()

# Drop the index and rename columns to make them more readable
table_data = table_data.reset_index(drop=True).rename(
    columns={
        'game_name': 'Title',
        'game_genres': 'Genres',
        'release_date': 'Release Date',
        'platform': 'Platform',
        'release_price': 'Price',
        'listing_url': 'Listing URL'
    }
)

# Ensure listing_url is in the DataFrame
if 'listing_url' in table_data.columns:
    # Create a new column for clickable game titles
    table_data['Title'] = table_data.apply(
        lambda row: f"<a href='{row['Listing URL']
                                }' target='_blank'>{row['Title']}</a>",
        axis=1
    )
else:
    raise ValueError(
        "The returned DataFrame does not contain the 'listing_url' column.")

# Drop the original 'game_name' column and rename the new column to 'Title'
table_data = table_data.drop(columns=['Listing URL']).rename(
    columns={'Title': 'Title'})

# Display the DataFrame
st.markdown(table_data.to_html(escape=False), unsafe_allow_html=True)
