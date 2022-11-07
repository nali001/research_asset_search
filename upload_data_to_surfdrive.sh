# Template bash script for uploading local data to the private Surfdrive storage space
# Rclone is required 
# Don't run this for once, 
# please navigate to corresponding folder that you want to upload data 
# and then use the relevant commands in this file to transfer data

# 1. 
# Source: data/pyserini
# Destination: /home/notebooksearch/data/pyserini
rclone copy ./pyserini na_surf:notebooksearch/data/pyserini  --progress

zip -r ./pyserini/collections.zip ./pyserini/collections
zip -r ./pyserini/indexes.zip ./pyserini/indexes
mkdir ./pyserini/temp
mv ./pyserini/*.zip ./pyserini/temp
cp ./pyserini/*.csv ./pyserini/temp
rclone copy ./pyserini/temp na_surf:notebooksearch/data/pyserini/  --progress
rm -dr ./pyserini/temp

