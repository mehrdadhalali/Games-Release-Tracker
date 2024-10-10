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


def execute_query(q: gql) -> str:
    """Executes a GraphQL query on a URL."""
    transport = AIOHTTPTransport(EPIC_URL)
    client = Client(transport=transport)
    result = client.execute(q)
    return dumps(result)


def get_listings_from_json(json_str: str) -> list[dict]:
    """Returns all game listing objects from the GraphQL response JSON."""
    data = loads(json_str.strip())
    return data['Catalog']['searchStore']['elements']


def get_operating_systems(tags: list[dict]):
    """Returns a list of operating systems from a list of tag dicts."""
    return [tag['name'] for tag in tags if tag.get('groupName') == "platform"]


def get_genres(tags: list[dict]):
    """Returns a list of genre from a list of API tags"""
    return [tag['name'] for tag in tags if tag.get('groupName') == "genre"]


def get_features(tags: list[dict]):
    """Returns all features from a list of tags"""
    return [tag['name'] for tag in tags if tag.get('groupName') == "feature"]


def format_release_date(release_date_str: str) -> str:
    """Returns a string formatted from UTC to %d/%m/%Y."""
    date_obj = datetime.fromisoformat(release_date_str.replace("Z", "+00:00"))
    return date_obj.strftime("%d/%m/%y")


def get_game_url(mappings: list[dict]) -> str:
    """Returns the game's URL from a list of mappings."""
    page_slug = mappings[0].get('pageSlug')
    return f"https://store.epicgames.com/en-US/p/{page_slug}"
