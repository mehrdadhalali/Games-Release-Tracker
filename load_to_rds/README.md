# 🚀 Transform and Load

This folder contains scripts to **transform** the data gathered by the web-scrapers, **load** it into the RDS, and **notify** users subscribed to games releases, about any newly released games of their favourite genres.

---

## 🛠️ Prerequisites

Ensure that you have the following:
- **Docker** installed for containerisation.
- **AWS CLI** configured to interact with AWS services (ECR, Lambda, RDS, etc.)
- **Python** installed on your local machine. 
---

## 📂 Setup

1. Create a `.env` file with the following content:

```bash
DB_HOST=XXXXX
DB_PORT=XXXXX
DB_PASSWORD=XXXXX
DB_USER=XXXXX
DB_NAME=XXXXX
```


## 📄 Files Explained

- `get_data_from_database.py`: To upload the data, we need to know some things about the already existing data, like IDs and duplicates. This script is for querying that data.
- `transform_game_data.py`: This is a short script that transforms the data received by the scrapers.
- `upload_to_db.py`: This script uploads all of the gathered data to the database.
- `test_load_to_rds`: Testing code.
- `delete.sql`: An SQL script to delete all game data (NOT metadata), executed by `clear_database.sh`
- `connect.sh`: Connects to the database. 