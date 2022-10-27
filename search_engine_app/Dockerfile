FROM python:3.8.15-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /search_engine_app
# Install psycopg dependencies
RUN apt-get install libpq-dev

# COPY requirements.txt requirements_dev.txt django_app_setup.sh settings_prod.py ./
COPY . .

RUN pip install -r requirements.txt -r requirements_dev.txt

CMD ["/bin/sh", "./django_app_setup.sh"]