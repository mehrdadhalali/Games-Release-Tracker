"""File to handle generating of the PDF report bytes object.
Defines a number of report sections as dynamically generated HTML."""

from datetime import datetime, timedelta
from io import BytesIO

from xhtml2pdf import pisa
from database_handler import (get_genre_listing_count, get_platform_listing_count,
                              get_platform_average_price, get_free_to_play)


def generate_report_header(current_date: datetime) -> str:
    """Generates the report header as an HTML string, automatically calculating the week range."""
    start_of_week = current_date - timedelta(days=current_date.weekday())
    end_of_week = start_of_week + timedelta(days=6)
    start_date_str = start_of_week.strftime("%d/%m/%y")
    end_date_str = end_of_week.strftime("%d/%m/%y")
    return f"""
    <html>
    <head>
        <title>Weekly Gaming Industry Report</title>
        {create_style_tag()}
    </head>
    <body>
        <h1>Weekly Gaming Industry Report</h1>
        <p>{start_date_str} - {end_date_str}</p>
    </body>
    """


def create_genre_table(genre_data: dict) -> str:
    """Creates an HTML table for the genre data."""
    table_html = """
    <h2>Breakdown by game genre:</h2>
    <table border="1" cellspacing="0" cellpadding="5">
        <thead>
            <tr>
                <th>Game Genre</th>
                <th>Number of Releases</th>
            </tr>
        </thead>
        <tbody>
    """
    for genre, count in genre_data.items():
        table_html += f"""
            <tr>
                <td>{genre}</td>
                <td>{count}</td>
            </tr>
        """
    table_html += """
        </tbody>
    </table>
    """
    return table_html


def create_game_summary(total_games: int, total_platforms: int) -> str:
    """Generates an HTML heading for the game release summary."""
    heading_html = f"""
    <h2>
        This week: <b>{total_games}</b>
        different games were released across
        <b>{total_platforms}</b> platforms.
    </h2>
    """
    return heading_html


def create_releases_table(platform_releases: dict) -> str:
    """Creates an HTML table for the total releases data."""
    table_html = """
    <h2>Releases per platform: </h2>
    <table border="1" cellspacing="0" cellpadding="5">
        <thead>
            <tr>
                <th>Platform</th>
                <th>Number of Releases</th>
            </tr>
        </thead>
        <tbody>
    """
    for platform, count in platform_releases.items():
        table_html += f"""
            <tr>
                <td>{platform}</td>
                <td>{count}</td>
            </tr>
        """
    table_html += """
        </tbody>
    </table>
    """

    return table_html


def create_pricing_table(platform_pricing: dict) -> str:
    """Creates an HTML table for the pricing data."""
    table_html = """
    <h2>Average price per platform: </h2>
    <table border="1" cellspacing="0" cellpadding="5">
        <thead>
            <tr>
                <th>Platform</th>
                <th>Average Price</th>
            </tr>
        </thead>
        <tbody>
    """
    for platform, price in platform_pricing.items():
        table_html += f"""
            <tr>
                <td>{platform}</td>
                <td>{price}</td>
            </tr>
        """
    table_html += """
        </tbody>
    </table>
    """

    return table_html


def create_free_to_play_table(free_to_play: dict) -> str:
    """Creates an HTML table for the free-to-play game data."""
    table_html = """
    <h2>Currently <b>Free to Play</b></h2>
    <table border="1" cellspacing="0" cellpadding="5">
        <thead>
            <tr>
                <th>Game Title</th>
                <th>Platform</th>
            </tr>
        </thead>
        <tbody>
    """
    for title, platform in free_to_play.items():
        table_html += f"""
            <tr>
                <td>{title}</td>
                <td>{platform}</td>
            </tr>
        """
    table_html += """
        </tbody>
    </table>
    """

    return table_html


def create_style_tag() -> str:
    """Returns a style tag with CSS for a cute design!"""
    with open("report_style", "r", encoding="UTF-8") as f:
        style = f.read().strip()
    return style


def convert_html_to_pdf(source_html):
    """Create a BytesIO object to hold the PDF data"""
    result_buffer = BytesIO()
    pisa.CreatePDF(source_html, dest=result_buffer)
    pdf_data = result_buffer.getvalue()
    result_buffer.close()
    return pdf_data


def create_report():
    """Gathers the data from the database handler and incrementally
    adds to the HTML string before converting it, and returning the bytes."""
    genre_dict = get_genre_listing_count()
    platform_dict = get_platform_listing_count()
    total_games = sum(platform_dict.values())
    total_platforms = len(platform_dict.keys())
    platform_price = get_platform_average_price()
    free_games = get_free_to_play()
    # Builds the HTML string
    template = (
        generate_report_header(datetime.now()) +
        create_game_summary(total_games, total_platforms) +
        create_releases_table(platform_dict) +
        create_genre_table(genre_dict) +
        create_pricing_table(platform_price) +
        create_free_to_play_table(free_games)
    )
    return convert_html_to_pdf(template)
