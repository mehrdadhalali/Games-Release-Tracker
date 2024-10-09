"""Script to web scrape the Steam new-releases page for new games."""

import re

import requests as req
import bs4

STEAM_NEW_RELEASE_URL = "https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998"
TIMEOUT = 10


def format_price(price_str: str) -> int:
    """Formats a price string and returns its value in pennies."""
    if price_str.strip().lower() == "free":
        return 0
    price_decimal = re.sub(r'[^\d.]', '', price_str)
    return int(float(price_decimal) * 100)


def load_page_source(url: str) -> str:
    """Returns the raw HTML string of a web-page's content."""
    response = req.get(url, timeout=TIMEOUT)
    if response.status_code != 200:
        raise ConnectionError(f"Failed to connect to {url}")
    return response.text


def get_page_listings(page_source: str) -> list[bs4.Tag]:
    """Returns a list of Steam game listing objects."""
    page_soup = bs4.BeautifulSoup(page_source, 'html.parser')
    search_result_rows = page_soup.find_all('a', class_='search_result_row')
    return search_result_rows


def parse_game_listing(game_listing: bs4.Tag) -> dict:
    """Parses game information from a game listing div."""
    url = game_listing.get('href')
    app_id = game_listing.get('data-ds-appid')
    img_tag = game_listing.find('img')
    img_src = img_tag.get('src') if img_tag else None
    title_tag = game_listing.find('span', class_='title')
    title = title_tag.text if title_tag else None
    release_tag = game_listing.find('div', class_='search_released')
    release_date = release_tag.text.strip() if release_tag else None
    price = game_listing.find(
        'div', class_='discount_final_price').text
    price = format_price(price)

    return {
        'app_id': app_id,
        'url': url,
        'img_url': img_src,
        'title': title,
        'release_date': release_date,
        'price': price
    }


if __name__ == "__main__":
    source = load_page_source(STEAM_NEW_RELEASE_URL)
    listings = get_page_listings(source)
    for listing in listings:
        print(parse_game_listing(listing))
