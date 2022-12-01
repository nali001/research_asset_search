from kagglecrawler import mongo_tools
task_number = 0
remote_path = f'notebook_search_docker/notebookcrawler/DB_exports/crawl_task_{task_number}/'
mongo_tools.auto_save(remote_path)