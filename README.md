# Notebook search engine backend
A search engine for various types of research assets. 
Right now it is focused on notebook search. 

------------------------------------------------------------------------------------------------------

## Deployment / Production
The deployment lives on docker and is accesible from the Internet. 

### Prerequisites 
- Open port 80/tcp
- Docker

### Usage
1. Setup environment on host machine, refer to `os_env_setup.sh`
2. Clone the repository \
`git clone https://github.com/nali001/notebook_search_docker.git`
3. Navigate to `notebook_search_docker` and run the following: 
```
mkdir elasticsearch/data elasticsearch/config elasticsearch/logs 
chmod g+rwx elasticsearch/data elasticsearch/config elasticsearch/logs 
sudo chgrp 0 elasticsearch/data elasticsearch/config elasticsearch/logs
```
3. Inside `search_engine_app/manage.py`, replace the following line: 
```
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'search_engine_app.settings')
```
4. Run 
```
docker compose up
```


------------------------------------------------------------------------------------------------------


## Development
Development is mainly for Django project.  

### Prerequisites 
- Conda
- Python 3.8
- Django 4.0
- Elsticsearch server


### Environment setup
1. Setup environment on host machine, refer to `os_env_setup.sh`
2. Clone the repository \
`git clone https://github.com/nali001/notebook_search_docker.git`
3. Setup local Python environment, refer to `search_engine_app/dev_env_setup.sh`
4. Start Elasticsearch service in a container \
`docker compose -f docker-compose_dev.yml up` \
It can be accessed via `localhost:9200`

Now you are good to go! Go to 
`search_engine_app` and run 
```
conda activate notebook_search
python manage.py runserver 7777
```

------------------------------------------------------------------------------------------------------
## Framework Design Philosophy 

### High-level structure 
![high-level structure](readme/high_level_structure.png)

### Network connection 
![high-level structure](readme/network.png)

### Storage 
![high-level structure](readme/storage.png)


------------------------------------------------------------------------------------------------------
## Folder explanation
### nginx
    - `opensemanticsearch/settings.py`: Django project global setting
    - `opensemanticsearch/settings.py`: URL configurations

+ `genericpages`: The main entry point of the search engine, containing a landing page

+ `notebookearch`: Notebook search module
+ `webSearch`: Web page searching module, including a crawler and a search engine
+ `DSS`: Crawler for datasets
    - `DSS/crawlerDatasetConfig.json`: Configuration file for the crawler. 

### elasticsearch 

### search_engine_app

### search_engine_app/notebook_search
The Django project, providing URL resolvement, data processing and web page generation

+ `notebook_indexing.py`: Feed preprocessed notebook files under `Jupyter Notebook` to Elasticsearch database


### docker-compose.yml 
Docker compose file for setting up **deployment** environment. 

### docker-compose.dev.yml 
Docker compose file for setting up **development** environment. 




-------------------------------------------------------------------------------------------------------
## Python-related tips
### Run scripts separately
Each djano app is considered as a package, we assume all the Python scripts are executed from `search_engine_app` dir. 

For example, if you wanna invoke `notebook_indexing` from CLI, use
```
python -m notebook_search.notebook_indexing.py
```

### Imports
+ Only use import for packages and modules, not classes or functions. 
+ Always use absolute path for importing modules even it is from the same package. 

In this case, you would not be confused by changing `sys.path`