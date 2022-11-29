# Template bash script for uploading local data to the private Surfdrive storage space
# Rclone is required 
# Don't run this for once, 
# please navigate to corresponding folder that you want to upload data 
# and then use the relevant commands in this file to transfer data

# 1. 
# Source: search_engine_app/notebooksearch/Raw_notebooks/
# Destination: /home/notebook_search_docker/Raw_notebooks
zip -r ./search_engine_app/notebooksearch/Raw_notebooks/Kaggle.zip ./search_engine_app/notebooksearch/Raw_notebooks/Kaggle
mkdir ./temp ./temp/logs
mv ./search_engine_app/notebooksearch/Raw_notebooks/Kaggle.zip ./temp
cp ./search_engine_app/notebooksearch/Raw_notebooks/logs/*.csv ./temp/logs
rclone copy ./temp na_surf:notebook_search_docker/Raw_notebooks/  --progress
rm -dr ./temp


# 2. 
# Source: search_engine_app/notebooksearch/Notebooks/
# Destination: /home/notebook_search_docker/Notebooks
mkdir ./temp
cp ./search_engine_app/notebooksearch/Notebooks/*.csv ./temp
rclone copy ./temp na_surf:notebook_search_docker/Notebooks/  --progress
rm -dr ./temp


# 3. 
# Source: notebookcrawler/DB_exports/
# Destination: /home/notebook_search_docker/notebookcrawler/DB_exports/
rclone copy ./notebookcrawler/DB_exports/ na_surf:notebook_search_docker/notebookcrawler/DB_exports/  --progress


# 4. 
# Source: notebookcrawler/Queries/
# Destination: /home/notebook_search_docker/notebookcrawler/Queries/
rclone copy ./notebookcrawler/Queries/ na_surf:notebook_search_docker/notebookcrawler/Queries/ --progress

