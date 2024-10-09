"""This script is for extracting all of the details of a single game on GOG."""

from datetime import datetime
from urllib.request import urlopen
from bs4 import BeautifulSoup


def get_html(url: str) -> str:
    """Return the html file of a given url."""

    page = urlopen(url)
    html_bytes = page.read()
    html = html_bytes.decode("utf_8")
    return html


def format_os(os_string: str) -> str:
    """Turns the OS into the proper format."""

    os_map = {
        "windows": "Windows",
        "mac": "Mac",
        "linux": "Linux"
    }

    os_string_lower = os_string.lower()
    operating_systems = []
    for key in os_map.keys():
        if key in os_string_lower:
            operating_systems.append(os_map[key])

    return operating_systems


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

    genres = []
    tags = []
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
            operating_systems = format_os(operating_systems)

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
