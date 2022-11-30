#---------------------- Setup Python 3.8 ----------------------#
conda create -n notebookcrawler python=3.8 -y
conda activate notebookcrawler

#---------------------- Install Python libraries ----------------------#
pip install -r requirements.txt

cp ./kagglecrawler/kaggle.json ~/.kaggle/kaggle.json
sudo chmod 600 /home/na/.kaggle/kaggle.json