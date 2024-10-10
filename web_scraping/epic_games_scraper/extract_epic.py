"""Extracting game data from Epic Games' GraphQL API."""

from json import dumps, loads
from datetime import datetime

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

EPIC_URL = "https://graphql.epicgames.com/graphql"


def load_graph_ql_query(file_name: str) -> gql:
    """Returns a GraphQL query from a file. Instantiates the 
    query with the current day."""
    with open(file_name, 'r', encoding='UTF-8') as file:
        query = file.read().strip()

    current_date = datetime.now().isoformat().split("T")[0]
    start_time = f"{current_date}T00:00:00.000Z"
    end_time = f"{current_date}T18:00:00.000Z"
    filter_string = f'[{start_time},{end_time}]'
    query = query.replace("{{RELEASE_DATE}}", filter_string)
    return gql(query)
