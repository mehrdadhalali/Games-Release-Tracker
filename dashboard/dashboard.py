"""
This is the main dashboard for the Games Tracker Streamlit application.
It includes data visualisations on the information collected from Steam, GOG and Epic,
which is stored in an AWS RDS database.
"""

import streamlit as st

# Page configuration
st.set_page_config(layout="wide")

st.title("Games Tracker")
