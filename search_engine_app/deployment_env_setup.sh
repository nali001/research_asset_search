python manage.py makemigrations
python manage.py migrate
python manage.py createsuperusr --noinput
gunicorn --bind :7777 --workers 4 search_engine_app.wsgi:application