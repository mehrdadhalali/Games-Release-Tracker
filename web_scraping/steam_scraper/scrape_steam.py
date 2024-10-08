"""Script to web scrape the Steam new-releases page for new games."""

import requests as req

STEAM_NEW_RELEASE_URL = "https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998"
TIMEOUT = 10


def load_page_source(url: str) -> str:
    """Returns the raw HTML string of a web-page's content."""
    response = req.get(url, timeout=TIMEOUT)
    if response.status_code != 200:
        raise ConnectionError(f"Failed to connect to {url}")
    return response.text


if __name__ == "__main__":
    print("Hello world!")
