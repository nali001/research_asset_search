# This is the project of query reformulation service

```bash
    
    docker-compose exec postgres psql --username=postgres  -c "CREATE DATABASE notebooksearch;"
    docker-compose exec postgres psql --username=postgres  -c "CREATE DATABASE logui;"  #--dbname=logui 

    docker compose up -d
    

    docker exec -it logui-http-worker-1 python manage.py createsuperuser --username=notebooksearch

```
