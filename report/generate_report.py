"""File to handle generating of the PDF report bytes object."""
from io import BytesIO
from datetime import datetime, timedelta

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import ParagraphStyle
from reportlab.platypus import Spacer


def get_table_style() -> TableStyle:
    """Returns a table style with a dark theme."""
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor("#7f5ace")),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('FONTNAME', (0, 0), (-1, 0), 'Courier-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.HexColor("#2E2E2E")),
        ('TEXTCOLOR', (0, 1), (-1, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 1, colors.HexColor("#6A0DAD")),
    ])


def create_heading(text: str) -> Paragraph:
    """Creates a heading paragraph with a dark theme."""
    heading_style = ParagraphStyle(
        name='HeadingStyle',
        fontName='Courier-Bold',
        fontSize=12,
        spaceAfter=12,
        alignment=0,
        textColor=colors.black,
    )
    return Paragraph(text, heading_style)


def create_genre_table(genre_data: dict) -> Table:
    """Creates a table for the genre data."""
    table_data = [['Game Genre', 'Number of Releases']]  # Table header
    for genre, count in genre_data.items():
        table_data.append([genre, count])
    genre_table = Table(table_data)
    genre_table.setStyle(get_table_style())
    return genre_table


def create_pricing_table(platform_pricing: dict) -> Table:
    """Creates a table for the pricing data."""
    pricing_table_data = [['Platform', 'Average Price']]
    for platform, price in platform_pricing.items():
        pricing_table_data.append([platform, price])
    pricing_table = Table(pricing_table_data)
    pricing_table.setStyle(get_table_style())
    return pricing_table


def create_releases_table(platform_releases: dict) -> Table:
    """Creates a table for the total releases data."""
    releases_table_data = [['Platform', 'Number of Releases']]
    for platform, count in platform_releases.items():
        releases_table_data.append([platform, count])
    releases_table = Table(releases_table_data)
    releases_table.setStyle(get_table_style())
    return releases_table


def create_free_to_play_table(free_to_play: dict) -> Table:
    """Creates a table for the free-to-play data."""
    free_table_data = [['Game Title', 'Platform']]
    for title, platform in free_to_play.items():
        free_table_data.append([title, platform])
    free_table = Table(free_table_data)
    free_table.setStyle(get_table_style())
    return free_table


def generate_summary_report_pdf(total_games: int, total_platforms: int, genre_data: dict,
                                platform_pricing: dict, platform_releases: dict,
                                free_games: dict) -> bytes:
    """Generates the structure of the attachment report from the given data."""
    date_range = get_date_range()
    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    story = build_story(total_games, total_platforms, genre_data,
                        platform_pricing, platform_releases, free_games, date_range)

    pdf.build(story)
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()
    return pdf_bytes


def get_date_range() -> str:
    """Returns the date range for the report."""
    today = datetime.now()
    seven_days_ago = today - timedelta(days=7)
    return f"{seven_days_ago.strftime('%d/%m/%Y')} - {today.strftime('%d/%m/%Y')}"


def build_story(total_games: int, total_platforms: int, genre_data: dict,
                platform_pricing: dict, platform_releases: dict,
                free_games: dict, date_range: str) -> list:
    """Builds the 'story' for creating the PDF document.
    Stories are incrementally appended to, and built to a PDF."""
    story = []
    spacer = Spacer(2, 20)
    story.append(create_heading(f"Gaming Trends: {date_range}"))
    story.append(create_heading(f'''This week: <b>{total_games}</b> different games
                                     were released across <b>{total_platforms}</b> platforms.'''))
    story.append(spacer)
    story.append(create_heading('Breakdown by Genre:'))
    story.append(create_genre_table(genre_data))
    story.append(spacer)
    story.append(create_heading('Average Price Per Platform:'))
    story.append(create_pricing_table(platform_pricing))
    story.append(spacer)
    story.append(create_heading('Total Releases by Platform:'))
    story.append(create_releases_table(platform_releases))
    story.append(spacer)
    story.append(create_heading('Free to Play Games:'))
    story.append(create_free_to_play_table(free_games))
    return story


def write_bytes_to_local_file(pdf_bytes: bytes):
    """Temporary function: writes PDF locally."""
    with open('report.pdf', 'wb') as file:
        file.write(pdf_bytes)
