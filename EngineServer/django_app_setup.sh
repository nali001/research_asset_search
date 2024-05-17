# change the settings to production
cp ./search_engine_app/settings_prod.py ./search_engine_app/settings.py


python manage.py makemigrations
python manage.py migrate

# python -m notebooksearch.notebook_indexing

gunicorn --bind :7777 --workers 4 search_engine_app.wsgi:application