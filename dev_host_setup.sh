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


#---------------------- Setup Environment variable ----------------------#
# Add the following to `~/.bashrc`
HOST_IP=localhost
ELASTICSEARCH_HOSTNAME=localhost
ELASTICSEARCH_PORT=9200
ELASTICSEARCH_USERNAME=elastic
ELASTICSEARCH_PASSWORD=changeme
POSTGRES_HOSTNAME=localhost
POSTGRES_PORT=5432
POSTGRES_USER=postgres
POSTGRES_PASSWORD=notebooksearch2022
POSTGRES_DB=notebooksearch