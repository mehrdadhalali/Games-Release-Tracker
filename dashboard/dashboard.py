"""
This is the main dashboard for the Games Tracker Streamlit application.
It includes data visualisations on the information collected from Steam, GOG and Epic,
which is stored in an AWS RDS database.
"""
from datetime import datetime

import streamlit as st

# Page configuration
st.set_page_config(layout="wide")

cols = st.columns([2, 1, 1])
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
        value=[default_start_date, default_end_date],   # Default range
        min_value=min_date,                               # Minimum selectable date
        max_value=today,                                  # Exclude future dates
        format="YYYY-MM-DD"
    )

    # Check if date_range has two dates to unpack
    if len(date_range) == 2:
        start_date, end_date = date_range
    else:
        st.warning("Please select both start and end dates.")

cols = st.columns([4, 1])
with cols[1]:
    show_nsfw = st.checkbox("Show NSFW Games")
