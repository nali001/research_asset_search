FROM python:3.8
COPY ./requirements.txt /app/requirements.txt
COPY ./kagglecrawler/ /app/

WORKDIR /app/
RUN pip install -r requirements.txt
ENTRYPOINT celery -A kagglecrawler worker --concurrency=20 --loglevel=info


