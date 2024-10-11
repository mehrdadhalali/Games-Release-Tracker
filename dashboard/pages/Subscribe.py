"""
This page includes the functionality for users to subscribe
and unsubscribe to email updates about game releases.
"""

import streamlit as st

st.set_page_config(layout="wide")

st.title("Subscribe to Games Tracker")

st.write("""Subscribe to stay updated! Select the types of content
          you're interested in, and we'll send you personalised email
          updates based on your preferences.""")

st.divider()

cols = st.columns([1.1, 2, 1])
with cols[0]:
    st.write("Receive our weekly report:")
with cols[1]:
    st.write("New game releases:")
with cols[2]:
    st.write("Include NSFW games:")

cols = st.columns([1.1, 1, 1, 1])

with cols[0]:
    weekly_report = st.checkbox("Weekly Report")

with cols[1]:
    indie = st.checkbox("Indie")
    action = st.checkbox("Action")
    casual = st.checkbox("Casual")
    adventure = st.checkbox("Adventure")
    simulation = st.checkbox("Simulation")
    rpg = st.checkbox("RPG")
    strategy = st.checkbox("Strategy")

with cols[2]:
    action_adventure = st.checkbox("Action-Adventure")
    sports = st.checkbox("Sports")
    racing = st.checkbox("Racing")
    software = st.checkbox("Software")
    early_access = st.checkbox("Early-Access")
    free_to_play = st.checkbox("Free-to-Play")
    massively_multiplayer = st.checkbox("Massively-Multiplayer")

with cols[3]:
    email_nsfw = st.checkbox("Include NSFW")
