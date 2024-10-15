"""This script creates an HTML, upon receiving a list of games, and their common genre."""
from json import load


def format_genre_text(genre: str) -> str:
    """Makes genre representable in an email."""

    if genre.lower() == "rpg":
        return "RPG"

    return genre.title()


def put_in_tag(body: str, tag_name: str,
               attrs="", is_single=False) -> str:
    """Puts something in a HTML tag."""
    body_in_tag = f"<{tag_name} {attrs}> {body}"
    if not is_single:
        body_in_tag += f"</{tag_name}>"
    return body_in_tag


def format_price(price: int) -> str:
    """Formats the price correctly."""
    if price == 0:
        return "FREE"
    price_str = round(price / 100, 2)
    return "£" + str(price_str)


def create_html(games: list[dict], genre: str) -> str:
    """Creates an HTML of the games of a specific genre."""
    message = put_in_tag(f"Here is all of the newly released games of the {format_genre_text(genre)} genre:",
                         "h1")
    for game in games:
        message += put_in_tag(put_in_tag(game["title"], "h2"),
                              "a", f"href={game["url"]}")
        message += put_in_tag(put_in_tag("", "img",
                              f"src={game["img_url"]}", is_single=True),
                              "a", f"href={game["url"]}") + "<br>"
        message += put_in_tag(
            f"Price: {format_price(game["current_price"])}", "h2")
        message += put_in_tag(f"Genre: {", ".join(game["genres"])}", "p")
        message += put_in_tag(game["description"], "p")
    message = put_in_tag(put_in_tag(message, "body"), "html")
    return message
