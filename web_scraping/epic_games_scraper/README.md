## Epic Games Extract
- Extracts data from Epic Games' **undocumented** GraphQL api.

## Setup
Please create an `.env` file with the following variables:
```bash
ECR_REPO_NAME=XXXXXX
AWS_ACCOUNT_ID=XXXXXX
```
- Run `bash push-to-ecr.sh`

## Files Explained
- `Dockerfile`: Used to build the image for this folder.
- `extract_epic.py`: Handles the extraction of data from the GraphQL api
- `lambda_handler.py`: The entry-point for the AWS Lambda function.
- `push-to-ecr.sh`: Handles the building, tagging, and pushing of the Docker image to the ECR repository.
- `query.graphql`: The GraphQL query used at the Epic Games API endpoint to retrieve data.
- `requirements.txt`: The Python dependencies for the project.
- `test_extract_epic.py`: Unit tests for the `extract_epic.py` file.