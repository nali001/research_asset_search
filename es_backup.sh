# Backup the Elasticsearch data and logs 
tar cvf ../es_backups/es_backup.tar ./elasticsearch/data ./elasticsearch/logs

# Restore the data and logs
# tar xvf ../es_backups/es_backup.tar -C ./
# chmod g+rwx elasticsearch/data elasticsearch/logs 
# sudo chgrp 0 elasticsearch/data elasticsearch/logs