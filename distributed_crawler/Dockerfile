FROM python:3.8
COPY ./requirements.txt /app/requirements.txt
ADD ./kagglecrawler/ /app/
# COPY ./kagglecrawler/kaggle.json /root/.kaggle/kaggle.json

WORKDIR /app/
RUN pip install -r requirements.txt
ENTRYPOINT celery -A kagglecrawler worker --concurrency=20 --loglevel=info


