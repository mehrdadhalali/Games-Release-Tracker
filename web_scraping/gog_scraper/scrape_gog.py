"""Script to scrape the latest games from GOG."""

from datetime import datetime

from bs4 import BeautifulSoup

from scrape_gog_game import get_game_data_from_url, get_html

BASE_URL = "https://www.gog.com/en/games?releaseStatuses=new-arrival&order=desc:releaseDate&hideDLCs=true&releaseDateRange=2024,2024&page="  # pylint: disable=C0301


def get_game_urls_from_page(page_html: str) -> list[str]:
    """Given a page, returns a list of all game URLs in that page."""
    soup = BeautifulSoup(page_html, "html.parser")
    links = soup.find_all("a", {"class": "product-tile"})
    return [link.get("href") for link in links]


def get_games_for_the_day(day: datetime = datetime.today(), page_number: int = 1) -> dict:
    """Get all of the details of the games for a given day."""
    url = BASE_URL + str(page_number)
    html = get_html(url)
    game_urls = get_game_urls_from_page(html)
    game_details_list = []
    for game_url in game_urls:
        game_details = get_game_data_from_url(game_url)
        if game_details["release_date"] < day:
            break
        if game_details["release_date"] == day:
            game_details["release_date"] = datetime.strftime(
                game_details["release_date"],
                "%d/%m/%Y")
            game_details_list.append(game_details)

    return {
        "platform": "gog",
        "listings": game_details_list
    }
