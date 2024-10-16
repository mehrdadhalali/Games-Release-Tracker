# Specifies latest image of python
FROM public.ecr.aws/lambda/python:latest

# Copies txt file containing env package requirements
COPY requirements.txt .

# Pip installs required packages.
RUN pip install -r requirements.txt

# Copies working files.
COPY get_data_from_database.py .
COPY lambda_handler.py .
COPY transform_game_data.py .
COPY upload_to_db.py .
COPY email_subscribers.py .
COPY get_subscriber_emails.py .
COPY create_html_message.py .



# Runs pipeline
CMD ["lambda_handler.lambda_handler"]