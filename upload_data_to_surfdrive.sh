# Template bash script for uploading local data to the private Surfdrive storage space
# Rclone is required 
# Don't run this for once, 
# please navigate to corresponding folder that you want to upload data 
# and then use the relevant commands in this file to transfer data

# 1.1 
# Source: search_engine_app/notebooksearch/Raw_notebooks/Kaggle
# Destination: /home/notebook_search_docker/Raw_notebooks
zip -r ./search_engine_app/notebooksearch/Raw_notebooks/Kaggle.zip ./search_engine_app/notebooksearch/Raw_notebooks/Kaggle
mkdir ./temp ./temp/Kaggle_logs
mv ./search_engine_app/notebooksearch/Raw_notebooks/Kaggle.zip ./temp
cp ./search_engine_app/notebooksearch/Raw_notebooks/logs/*.csv ./temp/Kaggle_logs
rclone copy ./temp na_surf:notebook_search_docker/Raw_notebooks/  --progress
rm -dr ./temp


# 1.2
# Source: search_engine_app/notebooksearch/Raw_notebooks/PWC
# Destination: /home/notebook_search_docker/Raw_notebooks
version=11
zip -r ./search_engine_app/notebooksearch/Raw_notebooks/PWC_${version}.zip ./search_engine_app/notebooksearch/Raw_notebooks/PWC
mkdir ./temp ./temp/PWC_logs_${version}
mv ./search_engine_app/notebooksearch/Raw_notebooks/PWC_${version}.zip ./temp
cp ./search_engine_app/notebooksearch/Raw_notebooks/PWC_logs/*.csv ./temp/PWC_logs_${version}
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


# 5. 
rclone copy ./notebooksearch/Notebooks/Kaggle_summarization_fake_score.csv na_surf:notebook_search_docker/./notebooksearch/Notebooks/ --progress


# ------------------------------------------------------------------------------------------------------
# 20 Sep 2023
# Source: data/notebook/Kaggle
# Destination: /home/notebook_search_docker/data/notebook/Kaggle
version=20_sep_2023
zip -r ./data/notebook/Kaggle_${version}.zip ./data/notebook/Kaggle
mv ./data/notebook/Kaggle_${version}.zip ./temp
rclone copy ./temp na_surf:notebook_search_docker/data/notebook/Kaggle  --progress
rm -dr ./temp


# 21 Sep 2023
# Source: data/dataset/Zenodo
# Destination: /home/notebook_search_docker/data/dataset/Zenodo
version=21_sep_2023
zip -r ./data/dataset/Zenodo/PWC_${version}.zip ./data/dataset/Zenodo/PWC
mkdir ./temp
mv ./data/dataset/Zenodo/PWC_${version}.zip ./temp/PWC_${version}.zip
cp -r ./data/dataset/Zenodo/PWC_logs ./temp/PWC_logs_${version}
rclone copy ./temp na_surf:notebook_search_docker/data/dataset/Zenodo  --progress
rm -dr ./temp


# 26 Sep 2023
# Source: data/dataset/Kaggle
# Destination: /home/notebook_search_docker/data/dataset/Kaggle
version=26_sep_2023
zip -r ./data/dataset/Kaggle/PWC_${version}.zip ./data/dataset/Kaggle/PWC
mkdir ./temp
mv ./data/dataset/Kaggle/PWC_${version}.zip ./temp/PWC_${version}.zip
cp -r ./data/dataset/Kaggle/PWC_logs ./temp/PWC_logs_${version}
rclone copy ./temp na_surf:notebook_search_docker/data/dataset/Kaggle  --progress
rm -dr ./temp


# 26 Sep 2023
# Source: data/notebook/Kaggle
# Destination: /home/notebook_search_docker/data/notebook/Kaggle
version=26_sep_2023
zip -r ./data/notebook/Kaggle/PWC_${version}.zip ./data/notebook/Kaggle/PWC
mkdir ./temp
mv ./data/notebook/Kaggle/PWC_${version}.zip ./temp/PWC_${version}.zip
cp -r ./data/notebook/Kaggle/PWC_logs ./temp/PWC_logs_${version}
rclone copy ./temp na_surf:notebook_search_docker/data/notebook/Kaggle  --progress
rm -dr ./temp