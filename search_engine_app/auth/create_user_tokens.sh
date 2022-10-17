# user: aubergine  
# token: 6239ff813e9b33b24f7bd60a59eb09d81f58df58
python manage.py createsuperuser --username aubergine  --email aubergine@notebooksearch.com
# password: notebooksearch2022

python manage.py drf_create_token aubergine


python manage.py createsuperuser --username admin  --email admin@notebooksearch.com
# password: notebooksearch2022

