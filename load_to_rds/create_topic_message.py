"""Turns out SNS doesn't support HTML, this is a placeholder script to just format the messages in a readable way."""

from json import load


def format_price(price: int) -> str:
    """Formats the price correctly."""

    if price == 0:
        return "FREE"

    return "£" + "%.2f" % (price/100)


def create_text_message(games: list[dict], genre: str):
    """Creates a text format of the message we're emailing."""

    message = f"Here are newly released {genre} games:\n\n"

    for game in games:
        message += f"""{game["title"]}:
            {format_price(game["current_price"])},
            available on {game["url"]}\n\n"""

    return message
