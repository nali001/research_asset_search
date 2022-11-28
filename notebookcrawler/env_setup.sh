#---------------------- Setup Python 3.8 ----------------------#
conda create -n notebookcrawler python=3.8 -y
conda activate notebookcrawler

#---------------------- Install Python libraries ----------------------#
pip install -r requirements.txt