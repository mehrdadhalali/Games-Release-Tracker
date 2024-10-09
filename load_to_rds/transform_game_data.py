"""This script is for transforming the data collected by the scrapers."""


NSFW_TAGS = ["psychedelic", "adult content", "hentai", "sexual content",
             "mature", "nudity", "nsfw"]


def has_nsfw_tags(game: dict) -> bool:
    """Does this game have any NSFW tags?"""

    return any(tag.lower() in NSFW_TAGS
               for tag in game["tags"])


def transform_to_tuples(game: dict) -> tuple:
    """Transform a game's details to tuples so that it can be inserted into the database."""
