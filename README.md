# Notebook search engine backend
A search engine for various types of research assets. 
Right now it is focused on notebook search. 

------------------------------------------------------------------------------------------------------

## Deployment / Production 
### Prerequisites 
- Open port 80/tcp
- Docker

### Usage
1. Setup environment on host machine, refer to `host_env_setup.sh`
2. Clone the repository
```
git clone --branch deploy https://github.com/nali001/notebook_search_docker.git
```

3. Prepare the data. Put your notebooks under `notebooksearch/Kaggle Notebook`

4. Run 
```
docker compose up
```
If the system does not work properly, either wait for some time for all containers to go up, or run `docker compose build` to update the images. 

Now you can access the web page on `http://IP_address/`

5. Initialize the web application via: `http://IP_address/api/initialize_app/`



### Administration
We expose `pgadmin` service to the localhost so that you can easily monitor the database. Access it through `http://localhost:5050/`

We expose `Django admin` service to public web. Access it through `http://IP_address/admin/` 


However, `postgres` `search_engine_app` and `Elasticsearch` services are only accessible within the docker network and thus cannot be accessed from the host machine or the web. 

Postgres pgadmin login 
```
Username: postgres@notebooksearch.com
Password: notebooksearch2022
```

Postgres pgadmin server connection
```
Hostname: postgres
Username: postgres
Password: notebooksearch2022
```

------------------------------------------------------------------------------------------------------
