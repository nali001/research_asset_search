# Template bash script for downloading data from the private Surfdrive storage space to local machine
# Rclone is required 
# Don't run this for once, 
# please navigate to corresponding folder that you want to download the data 
# and then use the relevant commands in this file to transfer data


# 1. 
# Source: search_engine_app/notebooksearch/Notebooks/
# Destination: /home/notebook_search_docker/Notebooks
rclone copy na_surf:notebook_search_docker/Notebooks/ ./search_engine_app/notebooksearch/Notebooks/ --progress
