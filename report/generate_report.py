"""File to handle generating of the PDF report bytes object."""
from io import BytesIO
from datetime import datetime, timedelta

from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet


def get_table_style() -> TableStyle:
    """Returns the table style used for the PDF document."""
    return TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black),
    ])


def create_heading(text: str, style: str) -> Paragraph:
    """Creates a heading paragraph."""
    styles = getSampleStyleSheet()
    return Paragraph(text, styles[style])


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


def generate_summary_report_pdf(total_games: int, total_platforms: int, genre_data: dict, platform_pricing: dict, platform_releases: dict) -> bytes:
    """Generates the structure of the attachment report from the given data."""
    today = datetime.now()
    seven_days_ago = today - timedelta(days=7)
    date_range = f"{seven_days_ago.strftime(
        '%d/%m/%Y')} - {today.strftime('%d/%m/%Y')}"

    pdf_buffer = BytesIO()
    pdf = SimpleDocTemplate(pdf_buffer, pagesize=letter)
    story = []
    story.append(create_heading(f"Gaming Trends: {date_range}", 'Heading1'))

    story.append(create_heading(f'This week: <b>{
                 total_games}</b> different games were released across <b>{total_platforms}</b> platforms.', 'Title'))
    story.append(create_heading('Breakdown by Genre:', 'Heading2'))
    story.append(create_genre_table(genre_data))

    story.append(create_heading('Average Price Per Platform:', 'Heading2'))
    story.append(create_pricing_table(platform_pricing))

    story.append(create_heading('Total Releases by Platform:', 'Heading2'))
    story.append(create_releases_table(platform_releases))
    pdf.build(story)
    pdf_bytes = pdf_buffer.getvalue()
    pdf_buffer.close()
    return pdf_bytes
