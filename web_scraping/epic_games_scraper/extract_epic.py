"""Extracting game data from Epic Games' GraphQL API."""

from json import dumps, loads
from datetime import datetime

from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport
from gql.transport.exceptions import TransportQueryError

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
    platforms = [tag['name'].replace("MacOS", "Mac").replace("Mac OS", "Mac")
                 for tag in tags if tag.get('groupName') == "platform"]
    return platforms


def get_genres(tags: list[dict]):
    """Returns a list of genre from a list of API tags"""
    return [tag['name'] for tag in tags if tag.get('groupName') == "genre"]


def get_features(tags: list[dict]):
    """Returns all features from a list of tags"""
    return [tag['name'] for tag in tags if tag.get('groupName') == "feature"]


def format_release_date(release_date_str: str) -> str:
    """Returns a string formatted from UTC to %d/%m/%Y."""
    date_obj = datetime.fromisoformat(release_date_str.replace("Z", "+00:00"))
    return date_obj.strftime("%d/%m/%Y")


def get_game_url(mappings: list[dict]) -> str:
    """Returns the game's URL from a list of mappings."""
    page_slug = mappings[0].get('pageSlug')
    return f"https://store.epicgames.com/en-US/p/{page_slug}"


def get_listing_image(image_list: list[dict]) -> str:
    """Returns the thumbnail image URL for a listing."""
    for img in image_list:
        if img['type'] == "Thumbnail":
            return img['url']
    return ""


def parse_listing(listing: dict) -> dict:
    """Parses a game listing, returns a formatted dictionary describing the game object."""
    return {
        "title": listing["title"],
        "description": listing["description"],
        "release_date": format_release_date(listing["releaseDate"]),
        "operating_systems": get_operating_systems(listing['tags']),
        "genres": get_genres(listing['tags']),
        "is_nsfw": False,  # Epic Games do not allow NSFW listings.
        "tags": get_features(listing['tags']),
        "current_price": listing["currentPrice"],
        "url": get_game_url(listing['mappings']),
        "img_url": get_listing_image(listing['keyImages'])
    }


def parse_listings(listings: list[dict]) -> dict:
    """Parses all listings, creates the output dictionary."""
    return {
        "platform": "epic",
        "listings": [parse_listing(listing) for listing in listings]
    }


def listing_is_game(categories: list[dict]) -> bool:
    """Returns true if a listing is a game. Filters out DLCs, soundtracks, etc."""
    non_game_keywords = {'addons', 'digitalextras',
                         'spthidden'}
    return not any(keyword in category['path']
                   for category in categories for keyword in non_game_keywords)


def write_json_to_file(json_str: str, file_name: str):
    """Writes a JSON string to a file locally."""
    json_obj = loads(json_str)
    so_pretty = dumps(json_obj, indent=4)
    with open(file_name, 'w', encoding="UTF-8") as f:
        f.write(so_pretty)


def process_listings(save_to_file: bool = False) -> None:
    """Main function to process listings. Optionally saves to a JSON file locally."""
    try:
        ql_query = load_graph_ql_query("query.graphql")
        response = execute_query(ql_query)
        all_listings = get_listings_from_json(response)
        game_listings = [listing for listing in all_listings
                         if listing_is_game(listing['categories'])]
    except (TransportQueryError):
        game_listings = []

    parsed = parse_listings(game_listings)
    if save_to_file:
        write_json_to_file(dumps(parsed), 'sample_output.json')
    return parsed


if __name__ == "__main__":
    process_listings(save_to_file=True)
