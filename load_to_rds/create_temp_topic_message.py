"""Turns out SNS doesn't support HTML, this is a placeholder script to just format the messages in a readable way."""

from json import load

from create_topic_message import format_price


def create_temp_message(games: list[dict], genre: str):
    """Creates a text format of the message we're emailing."""

    message = f"Here are newly released {genre} games:\n\n"

    for game in games:
        message += f"""{game["title"]}:
            {format_price(game["current_price"])},
            available on {game["url"]}\n\n"""

    return message


if __name__ == "__main__":

    with open("gog_data.json", "r") as f:

        games = load(f)

    with open("temp_message.txt", "w") as f:

        f.write(create_temp_message(
            games["listings"], "Cool"))
