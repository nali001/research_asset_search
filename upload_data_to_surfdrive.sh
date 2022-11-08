# Template bash script for uploading local data to the private Surfdrive storage space
# Rclone is required 
# Don't run this for once, 
# please navigate to corresponding folder that you want to upload data 
# and then use the relevant commands in this file to transfer data

# 1. 
# Source: search_engine_app/notebooksearch/Raw_notebooks/Kaggle
# Destination: /home/notebook_search_docker/Raw_notebooks
zip -r ./search_engine_app/notebooksearch/Raw_notebooks/Kaggle.zip ./search_engine_app/notebooksearch/Raw_notebooks/Kaggle
mkdir ./temp
mv ./search_engine_app/notebooksearch/Raw_notebooks/Kaggle.zip ./temp
cp ./search_engine_app/notebooksearch/Raw_notebooks/logs/*.csv ./temp
rclone copy ./temp na_surf:notebook_search_docker/Raw_notebooks/  --progress
rm -dr ./temp

