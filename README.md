# Notebook search engine backend
A search engine for various types of research assets. 
Right now it is focused on notebook search. 

------------------------------------------------------------------------------------------------------

## Deployment
The deployment lives on docker and is accesible from the Internet. 

### Prerequisites 
- Open port 80/tcp
- Docker

### Usage
1. Setup environment on host machine, refer to `os_env_setup.sh`
2. Clone the repository \
`git clone https://github.com/nali001/notebook_search_docker.git`
3. Run \
`docker compose up`


------------------------------------------------------------------------------------------------------


## Development
Development is mainly for Django project.  

### Prerequisites 
- Conda
- Python 3.8
- Django 4.0
- Elsticsearch server

Please refer to `search_engine_app/dev_env_setup.sh`


------------------------------------------------------------------------------------------------------
## Framework Design Philosophy 

### High-level structure 
![high-level structure](readme/high_level_structure.png)



### Folder explanation
+ important configuration files
    - `opensemanticsearch/settings.py`: Django project global setting
    - `opensemanticsearch/settings.py`: URL configurations

+ `genericpages`: The main entry point of the search engine, containing a landing page

+ `notebookearch`: Notebook search module
+ `webSearch`: Web page searching module, including a crawler and a search engine
+ `DSS`: Crawler for datasets
    - `DSS/crawlerDatasetConfig.json`: Configuration file for the crawler. 