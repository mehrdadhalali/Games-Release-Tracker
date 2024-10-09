"""Script to scrape the latest games from GOG."""

from time import perf_counter
from datetime import datetime
from bs4 import BeautifulSoup
from scrape_gog_game import get_game_data_from_url, get_html

BASE_URL = "https://www.gog.com/en/games?releaseStatuses=new-arrival&order=desc:releaseDate&hideDLCs=true&releaseDateRange=2024,2024&page="


def get_game_urls_from_page(page_html: str) -> list[str]:
    """Given a page, returns a list of all game URLs in that page."""

    soup = BeautifulSoup(page_html, "html.parser")

    links = soup.find_all("a", {"class": "product-tile"})

    return [link.get("href") for link in links]


def get_games_for_the_day(day: datetime = datetime.today(), page_number: int = 1) -> list[dict]:
    """Get all of the details of the games for a given day."""

    url = BASE_URL + str(page_number)

    html = get_html(url)

    game_urls = get_game_urls_from_page(html)

    game_details = list(map(get_game_data_from_url, game_urls))

    day_str = datetime.strftime(day, "%d/%m/%Y")

    relevant_games = [game for game in game_details
                      if game["release_date"] == day_str]

    return relevant_games


if __name__ == "__main__":

    start = perf_counter()
    games = get_games_for_the_day(day=datetime(2024, 10, 8))
    print(games[0])
    print(perf_counter() - start)
