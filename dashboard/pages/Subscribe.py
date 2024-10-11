"""
This page includes the functionality for users to subscribe
and unsubscribe to email updates about game releases.
"""

import re

import streamlit as st

# Regex for validating email
email_pattern = r'^[\w\.-]+@[\w\.-]+\.\w+$'

st.set_page_config(layout="wide")

st.title("Subscribe to Games Tracker")

st.write("""Subscribe to stay updated! Select the types of content
          you're interested in, and we'll send you personalised email
          updates based on your preferences.""")

st.divider()

cols = st.columns([1.1, 2, 0.8])
with cols[0]:
    st.write("Receive our weekly report:")
with cols[1]:
    st.write("New game releases:")
with cols[2]:
    st.write("Include NSFW games:")

cols = st.columns([1.1, 1, 1, 0.8])
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

cols = st.columns([1, 2, 1])
with cols[1]:
    st.write(" <br> ", unsafe_allow_html=True)

    email = st.text_input("Enter your email:")

    if st.button("Subscribe"):
        if re.match(email_pattern, email):
            st.success(f"You are subscribed with {email}. Bosh!")
        else:
            st.warning("Please enter a valid email address.")

st.divider()

cols = st.columns([1, 2, 1])
with cols[1]:
    with st.expander("Unsubscribe", expanded=False):
        unsubscribe_email = st.text_input(
            "Enter your email:", key="unsubscribe")
        if st.button("Unsubscribe"):
            if re.match(email_pattern, unsubscribe_email):
                st.success(f"You have unsubscribed {unsubscribe_email}.")
            else:
                st.warning("Please enter a valid email address.")
