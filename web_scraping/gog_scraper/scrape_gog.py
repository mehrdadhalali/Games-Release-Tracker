"""Script to scrape the latest games from GOG."""

from urllib.request import urlopen
from bs4 import BeautifulSoup
import requests as req

BASE_URL = "https://www.gog.com/en/games?releaseStatuses=new-arrival&order=desc:releaseDate&hideDLCs=true&releaseDateRange=2024,2024&page="


def get_html(url: str) -> str:
    """Return the html file of a given url."""

    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf_8")
    return html


def get_game_urls_from_page(page_html: str) -> list[str]:
    """Given a page, returns a list of all game URLs in that page."""

    soup = BeautifulSoup(page_html, "html.parser")

    links = soup.find_all("a", {"class": "product-tile"})

    return [link.get("href") for link in links]


def get_game_data_from_url(game_url: str) -> dict:
    """Given a game's URL, returns all of its relevant data."""

    soup = BeautifulSoup(get_html(game_url), "html.parser")

    title = soup.find(
        "h1", {"class": "productcard-basics__title"}).text.strip()

    description = soup.find(
        "div", {"class": "description"}).text.strip()

    image_url = soup.find("img", {"class": "mobile-slider__image"}).get("src")

    details_rows = soup.find_all("div", {"class": "table__row details__row"})
    for row in details_rows:
        row_label = row.find(
            "div", {"class": "details__category table__row-label"}).text

        if row_label == "Genre:":
            genre_links = row.find_all("a")
            genres = [link.text for link in genre_links]

        elif row_label == "Tags:":
            tag_links = row.find_all("a")
            tags = [link.text for link in tag_links]

    return {"title": title,
            "description": description,
            "image_url": image_url,
            "genres": genres,
            "tags": tags}


if __name__ == "__main__":

    url = BASE_URL + "1"
    html = get_html(url)

    urls = get_game_urls_from_page(html)

    print(get_game_data_from_url(urls[0]))
