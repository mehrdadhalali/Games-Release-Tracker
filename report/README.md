# Report Generator
A script to generate weekly summary reports of the games data collected.

## Features:
- Generates PDF files summarising key metrics for the past week:
- Emails subscribers with PDF report attachments

## Setup:

- Please ensure that a `.env` file exists in this directory with the following values:
```bash
DB_HOST=XXXXXX
DB_PORT=XXXXXX
DB_PASSWORD=XXXXXX
DB_USER=XXXXXX
DB_NAME=XXXXXX

FROM_EMAIL=XXXXXX
ECR_REPO_NAME=XXXXXX
AWS_REGION_NAME=XXXXXX
AWS_ACCOUNT_ID=XXXXXX
AWS_ACCESS_KEY=XXXXXX
AWS_SECRET_KEY=XXXXXX
```

- Please run `bash push-to-ecr.sh`


## Files Explained
- `Dockerfile`:
- `email_report.py`
- `generate_report.py`
- `lambda_handler.py`
- `push-to-ecr.sh`
- `requirements.txt`