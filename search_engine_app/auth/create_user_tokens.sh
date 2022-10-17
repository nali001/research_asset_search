# user: aubergine  
# token: ab132fc1bc7f55d8410d276335b5e922a7d60072
python manage.py createsuperuser --username aubergine  --email aubergine@notebooksearch.com
# password: notebooksearch2022

python manage.py drf_create_token aubergine


python manage.py createsuperuser --username admin  --email admin@notebooksearch.com
# password: notebooksearch2022

