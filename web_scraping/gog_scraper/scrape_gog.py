"""Script to scrape the latest games from GOG."""

from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup

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

    price_span = soup.find("span", {"selenium-id": "ProductFinalPrice"})

    if price_span is not None:

        price_str = price_span.text
    else:
        price_str = "0"

    current_price = int(float(price_str)*100)

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

    rating_rows = soup.find_all(
        "div", {"class": "table__row details__rating details__row"})

    for row in rating_rows:
        row_label = row.find(
            "div", {"class": "details__category table__row-label"}).text
        if "Works on:" in row_label:
            operating_systems = row.find(
                "div", {"class": "details__content table__row-content"}).text.strip()

        elif "Release date:" in row_label:
            release_date = row.find(
                "div", {"class": "details__content table__row-content"}).text.strip()

    release_date = datetime.strptime(release_date[3:13],
                                     "%Y-%m-%d")
    release_date = datetime.strftime(release_date,
                                     "%d/%m/%Y")

    return {"title": title,
            "description": description,
            "img_url": image_url,
            "genres": genres,
            "tags": tags,
            "operating_systems": operating_systems,
            "current_price": current_price,
            "release_date": release_date,
            "url": game_url}


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

    games = get_games_for_the_day(day=datetime(2024, 10, 8))
    print([game["title"] for game in games])
