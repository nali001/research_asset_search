FROM python:3.8.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /search_engine_app
# Install psycopg dependencies
RUN apt-get install libpq-dev

COPY ./requirements.txt ./requirements_dev.txt ./deployment_env_setup.sh ./
RUN pip install -r requirements.txt -r requirements_dev.txt

# COPY . .
# CMD ["gunicorn", "--bind", ":7777", "--workers", "4", "search_engine_app.wsgi:application"]
CMD ["source", "deployment_env_setup.sh"]