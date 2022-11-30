# Source: notebookcrawler/DB_exports/
# Destination: /home/notebook_search_docker/notebookcrawler/DB_exports/
rclone copy ./DB_exports/ na_surf:$1  --progress
