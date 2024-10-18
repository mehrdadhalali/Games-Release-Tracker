"""This script is for extracting all of the details of a single game on GOG."""

from datetime import datetime
from urllib.request import urlopen
import logging

from bs4 import BeautifulSoup

logger = logging.getLogger(__name__)


def get_html(url: str) -> str:
    """Return the html file of a given url."""
    with urlopen(url) as page:
        html_bytes = page.read()
        html = html_bytes.decode("utf_8")
        return html


def format_price(price_str: str) -> int:
    """Formats a price's string."""
    if "free" in price_str.lower():
        return 0
    return int(float(price_str)*100)


def find_price(price_div) -> int:
    """Given a div containing a game's price, finds said price."""
    price_str = price_div.find("span", {"selenium-id": "ProductFinalPrice"})
    if not price_str:
        price_str = price_div.find("span", {"class":
                                            "product-actions-price__final-amount"})
    if not price_str:
        raise ValueError("The price is somewhere else!")
    return format_price(price_str.text)


def format_os(os_string: str) -> str:
    """Turns the OS into the proper format."""
    os_list = ["windows", "mac", "linux"]
    os_string_lower = os_string.lower()
    operating_systems = []
    for os in os_list:
        if os in os_string_lower:
            operating_systems.append(os.title())
    return operating_systems


def extract_data_from_rows(rows: list[str], label_class: str, required_label: str,
                           item_class: str = None, are_links: bool = False):
    """Given a list of rows, written in the weird style of GOG's HTML,
        return only the items we're looking for."""
    for row in rows:
        row_label = row.find(
            "div", {"class": label_class}).text
        if required_label in row_label.lower():
            if not are_links:
                return row.find("div", {"class": item_class}).text.strip()
            links = row.find_all("a")
            return [link.text for link in links]
    return []


def has_nsfw_warning(game_page) -> bool:
    """Does this game have a NSFW warning?"""

    modules = game_page.find_all("p", {"class": "module"})

    if len(modules) == 0:
        return False

    if any("not appropriate for all ages" in module.text
           for module in modules):
        return True

    return False


def get_game_data_from_url(game_url: str) -> dict:
    """Given a game's URL, returns all of its relevant data.
        The only thing that needs processing afterwards is the release date."""
    logging.basicConfig(filename='myapp.log', level=logging.INFO)
    soup = BeautifulSoup(get_html(game_url), "html.parser")
    title = soup.find(
        "h1", {"class": "productcard-basics__title"}).text.strip()
    description = soup.find(
        "div", {"class": "description"}).text.strip()
    image_url = soup.find("img", {"class": "mobile-slider__image"}).get("src")
    price_div = soup.find("div", {"selenium-id":
                                  "ProductActionsBody"})
    current_price = find_price(price_div)
    details_rows = soup.find_all("div", {"class": "table__row details__row"})
    genres = extract_data_from_rows(details_rows,
                                    label_class="details__category table__row-label",
                                    required_label="genre", are_links=True)

    is_nsfw = has_nsfw_warning(soup)
    tags = extract_data_from_rows(details_rows,
                                  label_class="details__category table__row-label",
                                  required_label="tag", are_links=True)
    rating_rows = soup.find_all(
        "div", {"class": "table__row details__rating details__row"})
    operating_systems = extract_data_from_rows(rows=rating_rows,
                                               label_class="details__category table__row-label",
                                               required_label="works",
                                               item_class="details__content table__row-content",
                                               are_links=False)
    release_date = extract_data_from_rows(rows=rating_rows,
                                          label_class="details__category table__row-label",
                                          required_label="release",
                                          item_class="details__content table__row-content",
                                          are_links=False)
    operating_systems = format_os(operating_systems)
    try:
        release_date = datetime.strptime(release_date[3:13],
                                         "%Y-%m-%d")
    except TypeError:
        logger.info(f"The input to strptime was {release_date}")
    return {"title": title,
            "description": description,
            "img_url": image_url,
            "genres": genres,
            "is_nsfw": is_nsfw,
            "tags": tags,
            "operating_systems": operating_systems,
            "current_price": current_price,
            "release_date": release_date,
            "url": game_url}
