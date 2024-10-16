"""This is the script for the Streamlit app's Subscribe page."""

import re
from os import environ as ENV

from boto3 import client
import streamlit as st
from dotenv import load_dotenv

from pages.utils.subscribe_functions import (add_subscriber_to_rds, create_subscriber_chart,
                                             subscribe_user_to_topics, remove_subscriber_from_rds,
                                             unsubscribe_user_from_all_topics)

EMAIL_PATTERN = r'^[\w\.-]+@[\w\.-]+\.\w+$'

load_dotenv()
SNS_CLIENT = client(
    'sns', region_name=ENV["REGION"],
    aws_access_key_id=ENV["AWS_ACCESS_KEY"], aws_secret_access_key=ENV["AWS_SECRET_KEY"])

st.set_page_config(layout="wide")


st.title("Subscribe to Games Tracker")
st.write("""Subscribe to stay updated! Select the types of content
          you're interested in, and we'll send you personalised email
          updates based on your preferences.""")

st.divider()

cols = st.columns([1, 2])
with cols[0]:
    st.write("Receive our weekly report:")
with cols[1]:
    st.write("New game releases:")

cols = st.columns([1, 1, 1])
with cols[0]:
    weekly_report = st.checkbox("Weekly Report")

with cols[1]:
    # Mapping genres to SNS topics
    genre_topics = {
        "Indie": st.checkbox("Indie"),
        "Action": st.checkbox("Action"),
        "Casual": st.checkbox("Casual"),
        "Adventure": st.checkbox("Adventure"),
        "Simulation": st.checkbox("Simulation")
    }

with cols[2]:
    genre_topics_2 = {
        "RPG": st.checkbox("RPG"),
        "Strategy": st.checkbox("Strategy"),
        "Sports": st.checkbox("Sports"),
        "Racing": st.checkbox("Racing"),
        "Multiplayer": st.checkbox("Multiplayer")
    }

# Get the selected genres (those that are checked)
genre_topics.update(genre_topics_2)
selected_genres = [genre for genre, checked in genre_topics.items() if checked]

cols = st.columns([1, 2, 1])
with cols[1]:
    st.write(" <br> ", unsafe_allow_html=True)

    # Name input field
    name = st.text_input("Enter your name:")
    email = st.text_input("Enter your email:")

    if st.button("Subscribe"):
        if re.match(EMAIL_PATTERN, email):
            if weekly_report:
                if name:
                    add_subscriber_to_rds(name, email)
                else:
                    st.warning("Please enter your name to subscribe.")
            if selected_genres:  # Subscribe to selected genres
                subscribe_user_to_topics(SNS_CLIENT, email, selected_genres)
        else:
            st.warning("Please enter a valid email address.")

    st.markdown("<small>* NSFW content is not included in emails.</small>",
                unsafe_allow_html=True)

st.divider()

cols = st.columns([0.5, 2, 0.5])
with cols[1]:
    st.altair_chart(create_subscriber_chart(
        SNS_CLIENT, "c13-games"), use_container_width=True)

st.divider()

cols = st.columns([1, 2, 1])
with cols[1]:
    unsubscribe_expander = st.expander("Unsubscribe", expanded=False)

    unsubscribe_email = unsubscribe_expander.text_input(
        "Enter your email:", key="unsubscribe")

    if unsubscribe_expander.button("Unsubscribe"):
        if re.match(EMAIL_PATTERN, unsubscribe_email):
            remove_subscriber_from_rds(unsubscribe_email)
            unsubscribe_user_from_all_topics(SNS_CLIENT, unsubscribe_email)
        else:
            st.warning("Please enter a valid email address.")
