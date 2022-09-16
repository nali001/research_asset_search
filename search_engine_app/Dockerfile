FROM python:3.8.10

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /search_engine_app
COPY ./requirements.txt .
COPY ./requirements_dev.txt .
RUN pip install -r requirements.txt -r requirements_dev.txt
RUN python -m notebook_search.notebook_indexing

# COPY . .

CMD ["gunicorn", "--bind", ":7777", "--workers", "4", "search_engine_app.wsgi:application"]
