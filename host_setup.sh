# For setting up Elasticsearch
#--- 1. Change the memory limit
sudo nano /etc/sysctl.conf
# add this line at the bottom: vm.max_map_count=262144


#--- 2. Modify access rights for the elasticsearch data
mkdir elasticsearch/data elasticsearch/config elasticsearch/logs 
chmod g+rwx elasticsearch/data elasticsearch/config elasticsearch/logs 
sudo chgrp 0 elasticsearch/data elasticsearch/config elasticsearch/logs

