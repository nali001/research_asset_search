
# Notebook Crawler
The crawler is used for scraping notebooks from Kaggle platform 

Two main assets are: 
- `distributed_notebook_crawling.py`
- `distribute_tasks.py`

`distributed_notebook_crawling.py` is to start a crawler on a single machine with multiple processes. 

`distribute_tasks.py` is to split and load tasks for multiple machines. 

------------------------------------------------------------------------------------------------------
## Environment setup
Refer to `env_setup.sh`

------------------------------------------------------------------------------------------------------
## Single machine usage
Steps: 
1. Modify the following control parameters according to your need: 
```
re_search = False
task_number = 0       
span = 100
task_name = 'search'
```

2. Navigate to `notebookcrawler` and run
```
python -m kagglecrawler.distributed_notebook_crawling
```

To use nohup: 
```
nohup python -m kagglecrawler.distributed_notebook_crawling
```

------------------------------------------------------------------------------------------------------
## Multi-machine usage
Machines better to have different IP addresses. 
Steps: 
1. Split the XXX (either `search` or `crawl`) tasks in a master machine. \
Uncomment `split_XXX_tasks()` within `kagglecrawler/distribute_tasks.py`, navigate to `notebookcrawler` and run 
```
python -m kagglecrawler.distribute_tasks
```

2. Load tasks in each worker machine. \
Uncomment `load_tasks()` within `kagglecrawler/distribute_tasks.py`, navigate to `notebookcrawler` and run 
```
python -m kagglecrawler.distribute_tasks
```

3. Follow single machine usage instructions

------------------------------------------------------------------------------------------------------
## Database monitor 
`kagglecrawler/mongo_tools` offers the following tools for monitoring the database: 
- real_time_status()
- get_coll_status()

Uncomment the function(s) in need, navigate to `notebookcrawler` and run 
```
python -m kagglecrawler.mongo_tools
```

------------------------------------------------------------------------------------------------------
## Data backup
`kagglecrawler/mongo_tools` provides `auto_save()` function to export all the collections and upload them to surfdrive implemented by `upload_task_data.sh`