"""Creates the message that gets emailed to subscribers."""

# pylint: disable=C0209


def format_genre_text(genre: str) -> str:
    """Makes genre representable in an email."""

    if genre.lower() == "rpg":
        return "RPG"

    return genre.title()


def format_price(price: int) -> str:
    """Formats the price correctly."""

    if price == 0:
        return "FREE"

    return f"£{"%.2f" % (price/100)}"


def create_text_message(games: list[dict], genre: str):
    """Creates a text format of the message we're emailing."""

    message = f"Here are newly released {format_genre_text(genre)} games:\n\n"

    for game in games:
        message += f"""{game["title"]}:
            {format_price(game["current_price"])},
            available on {game["url"]}\n\n"""

    return message


if __name__ == "__main__":
    print(format_price(1350))
