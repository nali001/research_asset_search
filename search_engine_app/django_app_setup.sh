python manage.py makemigrations
python manage.py migrate
python manage.py collectstatic
copy ./search_engine_app/settings_prod.py ./search_engine_app/settings.py
# change the settings
gunicorn --bind :7777 --workers 4 search_engine_app.wsgi:application