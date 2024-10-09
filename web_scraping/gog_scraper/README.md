# 🚀 GOG Scraper

This folder contains scripts to **scrape** the latest games from [the GOG website.](https://www.gog.com/en/games?releaseStatuses=new-arrival&order=desc:releaseDate&hideDLCs=true)

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
AWS_ACCOUNT_ID=XXXXX
ECR_REPO_NAME=XXXXX
```

2. Run `bash dockerise.sh`


## 📄 Files Explained
- `scrape_gog.py`: Scrapes the main page of GOG to get the URL's of the newest games.
- `scrape_gog_game.py`: Scrapes a single game's data from GOG.
- `lambda_handler`: The Lambda handler script.
- `test_scrape_gog.py`: Test files.
- `Dockerfile`: Instructions for Dockerisation.
- `dockerise.sh`: Containerises the scripts.