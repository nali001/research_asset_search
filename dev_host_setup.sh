#---------------------- Setup Conda ----------------------#
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh 
bash Miniconda3-latest-Linux-x86_64.sh
rm Miniconda3-latest-Linux-x86_64.sh

#---------------------- Setup Python 3.8 ----------------------#
conda create -n notebook_search python=3.8 -y
conda activate notebook_search

#---------------------- Install Python libraries ----------------------#
pip install -r requirements.txt
pip install -r requirements_dev.txt


#--------------------- Setup environment variables----------------------#
export HOST_IP=localhost
export ELASTICSEARCH_HOSTNAME=localhost
export ELASTICSEARCH_PORT=9200
export ELASTICSEARCH_USERNAME=elastic
export ELASTICSEARCH_PASSWORD=changeme
export POSTGRES_HOSTNAME=localhost
export POSTGRES_PORT=5432
export POSTGRES_USER=postgres
export POSTGRES_PASSWORD=notebooksearch2022
export POSTGRES_DB=notebooksearch