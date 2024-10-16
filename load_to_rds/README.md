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
MY_AWS_ACCESS_KEY=XXXXX
MY_AWS_SECRET_ACCESS_KEY=XXXXX
SNS_TOPIC_PREFIX=XXXXX
AWS_ACCOUNT_ID=XXXXX
ECR_REPO_NAME=XXXXX
SENDER_EMAIL_ADDRESS=XXXXX
```
2. Using a virtual environment, or otherwise, run `pip install python-dotenv boto3`.
3. To create the SNS topics for the genres, run `python3 create_sns_topics.py`.
4. Run `bash dockerise.sh`.

## 📄 Files Explained
### Loading data into the database
- `get_data_from_database.py`: To upload the data, we need to know some things about the already existing data, like IDs and duplicates. This script is for querying that data.
- `transform_game_data.py`: This is a short script that transforms the data received by the scrapers.
- `upload_to_db.py`: This script uploads all of the gathered data to the database.
### Sending emails to subscribers
- `get_subscriber_emails.py`: Receives the emails of all subscribers for each genre from their SNS topics.
- `create_html_message.py`: Given a list of games and their details, creates emails containing them, in HTML format.
- `email_subscribers.py`: Given the scraped data, combines the scripts above to email the subscribers.
### Misc.
- `lambda_handler.py`: The script run when the AWS lambda is triggered.
- `create_sns_topics.py`: A script for initialising the SNS topics on AWS. This script acts as a schema for the SNS topics and needs to be run exactly once before anything else is executed.
- `test_load_to_rds.py`: Testing code.
- `delete.sql`: An SQL script to delete all game data (NOT metadata), executed by `clear_database.sh`
- `connect.sh`: Connects to the database. 
- `dockerise.sh`: Dockerises the scripts.
- `Dockerfile`: Instructions for dockerisation.