#---------------------- Setup Conda ----------------------#
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh 
bash Miniconda3-latest-Linux-x86_64.sh
rm Miniconda3-latest-Linux-x86_64.sh

#---------------------- Setup Python 3.8 ----------------------#
conda create -n notebook_search python=3.8 -y
conda activate notebook_search

#---------------------- Install Python libraries ----------------------#
pip install -r requirements.txt
pip install -r requirements.dev.txt