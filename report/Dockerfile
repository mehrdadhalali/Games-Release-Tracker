FROM public.ecr.aws/lambda/python:latest

WORKDIR ${LAMBDA_TASK_ROOT}

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY generate_report.py .
COPY email_report.py .
COPY database_handler.py .
COPY lambda_handler.py .

CMD ["lambda_handler.lambda_handler"]