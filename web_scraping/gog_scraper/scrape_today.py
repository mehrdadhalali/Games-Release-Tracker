from json import dump
from scrape_gog import get_games_for_the_day
from datetime import datetime

if __name__ == "__main__":

    data = get_games_for_the_day(datetime(2024, 10, 18))

    with open("gog_data_new.json", "w") as f:
        dump(data, f, indent=4)
