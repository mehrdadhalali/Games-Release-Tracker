# pylint: disable=E0401
"""
This is the Games pages of the application, where users can search
for games, compare the prices, and get directed to their chosen platform.
"""

from datetime import datetime

import streamlit as st

from functions import display_game_table

# Page configuration
st.set_page_config(layout="wide")

st.markdown(
    """
    <style>
    a {
        color: #A26ED5 !important;  /* Override the link color */
    }
    </style>
    """,
    unsafe_allow_html=True)

cols = st.columns([2, 0.75, 1, 0.35])
with cols[0]:
    st.title("List of Games")
with cols[1]:
    os_selection = st.selectbox(
        "Operating System:",
        options=["-All-", "Windows", "Mac", "Linux"]
    )
with cols[2]:
    today = datetime.now().date()
    min_date = datetime(2024, 10, 1).date()
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

cols = st.columns([2, 1])
with cols[0]:
    # Create a search box
    search_query = st.text_input("Search for a game:", "")
with cols[1]:
    # Create dropdown for sorting
    sort_by = st.selectbox("Sort by:", options=[
        "", "Price (Lowest)", "Price (Highest)", "Title (A-Z)", "Title (Z-A)", "Date (Newest)", "Date (Oldest)"])

# Game releases table
display_game_table(show_nsfw, os_selection, start_date,
                   end_date, search_query, sort_by)
