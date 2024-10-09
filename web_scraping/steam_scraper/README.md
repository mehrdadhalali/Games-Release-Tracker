# 🎮 Steam Scraper

Automated solution to scrape the Steam new-releases page, packaged with Docker and deployed with AWS.

---

## 🚀 Prerequisites

Before you start, make sure the following tools are installed and configured:

- **🐳 Docker** – To containerize and run the application.
- **☁️ AWS CLI** – To interact with AWS services (ECR, Lambda, RDS, etc.).
- **🐍 Python** – Ensure Python is installed for managing dependencies and scripts.

---

## ⚙️ Setup Instructions

Follow these steps to get started:

1. **Create an `.env` file** in the root directory with these values:

   ```bash
   ECR_REPO_NAME=XXXXXX
   AWS_ACCOUNT_ID=XXXXXX
   ```

2. **Set up a virtual environment**
- Create and activate the virtual environment
- Navigate to the project's directory

3. **Install the required dependencies**
- Run `pip3 install -r requirements.txt`

4. **Push to AWS ECR**:
Run the following bash command to build, tag, and push the Docker image to AWS Elastic Container Registry (ECR)

`bash push-to-ecr.sh`

## 🗂️ File Structure

- `lambda_handler.py`: The script run when the AWS lambda is triggrered.
- `scrape_steam.py`: The file containing the main logic for the Steam web-scraping.
- `Dockerfile`: The file for building the Docker image.
- `push-to-ecr.sh`: The bash file for building, running, and pushing the Docker image to an ECR repository.


### Note
- Please ensure that AWS credentials are properly configured for the CLI to interact with the AWS account.