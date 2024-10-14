"""
This is the "About" page of the dashboard, including information about the project and dashboard.
"""

import streamlit as st

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

# Title
st.title("About Games Tracker")

# Contents
cols = st.columns([1, 3])

with cols[0]:
    st.image("pages/logo.png", width=250)

with cols[1]:
    st.write(" <br> ", unsafe_allow_html=True)
    st.write("""Games Tracker is a comprehensive tool designed to help gamers discover new releases
            across multiple PC gaming platforms, including Steam, GOG, and Epic Games.
            Our mission is to provide an intuitive interface that allows users to track
            the latest game releases, analyse trends, and stay informed about the gaming landscape.
            With a focus on user experience, Games Tracker aims to empower gamers and developers alike
            by offering valuable insights into the ever-evolving world of gaming.""")

st.subheader("Stay Updated with the Latest Gaming Trends")

st.write("""Navigating the Games Tracker dashboard is easy! On the Dashboard, you'll find a user-friendly
         interface displaying the latest game releases, trending categories, and insightful analytics.
         You can filter games by operating system and release date to find exactly what you're looking for.
         To receive updates on new releases in your favorite genres, simply subscribe by navigating 
         to the Subscribe page on the sidebar. You'll receive email notifications whenever
         a new game is added, ensuring you never miss out on the latest gaming experiences.""")

st.subheader("Contact us")

st.write("""We value your feedback and are here to assist you! If you have any questions, suggestions,
         or encounter any issues while using Games Tracker, please don't hesitate to reach out to us. 
         You can contact our support team via email at support@gamestracker.com. We are committed to 
         providing you with the best gaming experience and look forward to hearing from you!""")
