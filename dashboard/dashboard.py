# pylint: disable=C0103
# pylint: disable=W0621
"""
This is the main dashboard for the Games Tracker Streamlit application.
It includes data visualisations on the information collected from Steam, GOG and Epic,
which is stored in an AWS RDS database.
"""
from datetime import datetime

import streamlit as st

from functions import create_donut_chart, create_genre_bar_chart, create_line_chart, create_os_bar_chart, create_platform_bar_chart, create_release_line_chart, display_game_table

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
    unsafe_allow_html=True)  # Change hyperlink colour

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

    st.markdown("<small>* See the full list of available games <a href='Games'>here</a></small>",
                unsafe_allow_html=True)

    # Changing stats
    cols = st.columns(2)
    with cols[0]:
        st.altair_chart(create_platform_bar_chart(os_selection, start_date, end_date, show_nsfw),
                        use_container_width=True)
    with cols[1]:
        st.altair_chart(create_os_bar_chart(
            os_selection, start_date, end_date), use_container_width=True)

    if start_date != end_date:
        cols = st.columns(2)
        with cols[0]:
            st.altair_chart(create_release_line_chart(show_nsfw, start_date, end_date),
                            use_container_width=True)
        with cols[1]:
            st.altair_chart(create_genre_bar_chart(show_nsfw, start_date, end_date),
                            use_container_width=True)


    # All time stats
    st.subheader("All Time Stats")
    st.markdown(
        "<style>.line { border: 0.5px solid; margin: 0; }</style><div class='line'></div>",
        unsafe_allow_html=True)

    cols = st.columns(2)
    with cols[0]:
        st.altair_chart(create_donut_chart(), use_container_width=True)
    with cols[1]:
        st.altair_chart(create_line_chart(), use_container_width=True)

    st.subheader("List of Games")
    st.markdown(
        "<style>.line { border: 0.5px solid; margin: 0; }</style><div class='line'></div>",
        unsafe_allow_html=True)

    # Game releases table
    display_game_table(show_nsfw, os_selection, start_date, end_date)
