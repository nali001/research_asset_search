FROM python:3.8.15-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /search_engine_app

# install dependencies
RUN pip install --upgrade pip

# Install psycopg dependencies
RUN apt-get install libpq-dev

COPY ./requirements.txt .
COPY ./requirements_dev.txt .

RUN pip install -r requirements.txt -r requirements_dev.txt

# copy entrypoint.sh
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' /search_engine_app/entrypoint.sh
RUN chmod +x /search_engine_app/entrypoint.sh


# COPY requirements.txt requirements_dev.txt django_app_setup.sh settings_prod.py ./
# COPY . .

# run entrypoint.sh
ENTRYPOINT ["/search_engine_app/entrypoint.sh"]