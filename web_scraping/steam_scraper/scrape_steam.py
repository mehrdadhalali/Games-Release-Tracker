"""Script to web scrape the Steam new-releases page for new games."""

from json import dumps
from datetime import datetime
import re

import requests as req
import bs4

STEAM_NEW_RELEASE_URL = "https://store.steampowered.com/search/?sort_by=Released_DESC&category1=998"
STEAM_APP_URL = "https://store.steampowered.com/app/"
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
        raise ConnectionError(f"Failed to connect to {url}.")
    return response.text


def get_page_listings(page_source: str) -> list[bs4.Tag]:
    """Returns a list of Steam game listing objects released on a certain date."""
    page_soup = bs4.BeautifulSoup(page_source, 'html.parser')
    search_result_rows = page_soup.find_all('a', class_='search_result_row')
    return search_result_rows


def filter_timely_listings(listings: list[bs4.Tag], filter_date: datetime) -> list[bs4.Tag]:
    """Filters game release listings to match a given date."""
    timely_listings = []
    for listing in listings:
        release_date = parse_release_date(listing)
        if release_date and release_date.date() == filter_date.date():
            timely_listings.append(listing)

    return timely_listings


def parse_game_url(game_listing: bs4.Tag) -> str:
    """Extracts the URL from the game listing."""
    return game_listing.get('href')


def parse_app_id(game_listing: bs4.Tag) -> str:
    """Extracts the App ID from the game listing."""
    return game_listing.get('data-ds-appid')


def parse_image_url(game_listing: bs4.Tag) -> str:
    """Extracts the image URL from the game listing."""
    img_tag = game_listing.find('img')
    return img_tag.get('src') if img_tag else None


def parse_title(game_listing: bs4.Tag) -> str:
    """Extracts the title from the game listing."""
    title_tag = game_listing.find('span', class_='title')
    return title_tag.text if title_tag else None


def parse_release_date(game_listing: bs4.Tag) -> datetime:
    """Extracts the release date from the game listing."""
    release_tag = game_listing.find('div', class_='search_released')
    release_date_str = release_tag.text.strip() if release_tag else None
    date_formats = [
        '%d %B, %Y',
        '%B %Y',
        '%d %b, %Y',
        '%Y-%m-%d'
    ]

    if release_date_str:
        for format in date_formats:
            try:
                return datetime.strptime(release_date_str, format)
            except ValueError:
                pass
    return None


def parse_price(game_listing: bs4.Tag) -> str:
    """Extracts the price from the game listing and formats it."""
    price_tag = game_listing.find('div', class_='discount_final_price')
    price = price_tag.text if price_tag else None
    return format_price(price)


def get_steam_app_url(app_id: str) -> str:
    """Formats the base steam url for a particular app."""
    return f"{STEAM_APP_URL}{app_id}/"


def scrape_game_description(app_soup: bs4.BeautifulSoup) -> str:
    """Scrapes a game's Steam app page for description information."""
    description_tag = app_soup.find('div', class_='game_description_snippet')
    if description_tag:
        return description_tag.text.strip()
    return "No description available."


def scrape_game_tags(app_soup: bs4.BeautifulSoup) -> list[str]:
    """Scrapes a game's Steam app page for tags."""
    tag_elements = app_soup.find_all('a', class_='app_tag')
    tags = [tag.text.strip() for tag in tag_elements]
    return tags if tags else ["No tags available."]


def scrape_game_genres(app_soup: bs4.BeautifulSoup) -> list[str]:
    """Scrapes a game's Steam app page for genres."""
    genres_section = app_soup.find('div', id='genresAndManufacturer')
    if genres_section:
        genre_elements = genres_section.find_all('a', href=True)
        genres = [genre.text.strip()
                  for genre in genre_elements if "genre" in genre['href']]
    return genres if genres else []


def scrape_game_operating_systems(app_soup: bs4.BeautifulSoup) -> list[str]:
    """Scrapes a game's Steam app page for supported operating systems."""
    platform_mapping = {
        'win': 'Windows',
        'mac': 'Mac',
        'linux': 'Linux'
    }
    platforms = []
    platform_elements = app_soup.find_all('span', class_='platform_img')

    for platform in platform_elements:
        if 'class' in platform.attrs and len(platform['class']) > 1:
            platform_class = platform['class'][1]
            if platform_class in platform_mapping:
                platforms.append(platform_mapping[platform_class])

    return platforms if platforms else []


def parse_game_listing(game_listing: bs4.Tag) -> dict:
    """Parses game information from a game listing div."""
    app_id = parse_app_id(game_listing)
    steam_app = get_steam_app_url(app_id)
    steam_app_page_source = load_page_source(steam_app)
    app_soup = bs4.BeautifulSoup(steam_app_page_source, 'html.parser')

    return {
        'title': parse_title(game_listing),
        'description': scrape_game_description(app_soup),
        'release_date': datetime.strftime(parse_release_date(game_listing), '%d %b %Y'),
        'operating_systems': scrape_game_operating_systems(app_soup),
        'genres': scrape_game_genres(app_soup),
        'tags': scrape_game_tags(app_soup),
        'current_price': parse_price(game_listing),
        'url': parse_game_url(game_listing),
        'img_url': parse_image_url(game_listing),
    }


def collect_and_parse_games(scrape_date: datetime = None) -> str:
    """Collects the listings and parses them for information, adding them
    to an overall dictionary which is returned a JSON string for the lambda."""
    source = load_page_source(STEAM_NEW_RELEASE_URL)
    listings = get_page_listings(source)
    if scrape_date:
        listings = filter_timely_listings(listings, scrape_date)
    listings_dict = {
        "platform": "steam",
        "listings": [parse_game_listing(x) for x in listings]
    }
    return dumps(listings_dict)


print(collect_and_parse_games(datetime.now()))
