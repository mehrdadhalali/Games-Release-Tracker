# 📊 Report Generator
A script to generate weekly summary reports of the games data collected.

## ✨ Features:
- Generates PDF files summarising key metrics for the past week.
- Emails subscribers with PDF report attachments.

## ⚙️ Setup:

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
MY_AWS_ACCESS_KEY=XXXXXX
MY_AWS_SECRET_KEY=XXXXXX
```

- Run `bash push-to-ecr.sh`


## 📁 Files Explained
- `Dockerfile`: Contains instructions to build the Docker image
- `email_report.py`: Handles email functionality for sending reports.
- `generate_report.py`: Generates the PDF report for summarising the game data.
- `lambda_handler.py`: AWS Lambda entry point for triggering the report generation.
- `push-to-ecr.sh`: Script to build, tag, and push the Docker image to the AWS ECR repository.
- `requirements.txt`: Lists the Python dependencies for the project.