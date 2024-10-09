# Specifies latest image of python
FROM public.ecr.aws/lambda/python:latest

# Copies txt file containing env package requirements
COPY requirements.txt .

# Pip installs required packages.
RUN pip install -r requirements.txt

# Copies working files.
COPY lambda_handler.py .
COPY scrape_gog_game.py .
COPY scrape_gog.py .

# Runs pipeline
CMD ["lambda_handler.lambda_handler"]