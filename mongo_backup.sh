# Ref: https://pymongo.readthedocs.io/en/stable/examples/copydb.html
mongodump --archive="mongobackup-kagglecrawler" --db=kagglecrawler
mongorestore --archive="mongobackup-kagglecrawler" --nsFrom='kagglecrawler.*' --nsTo='kagglecrawler.*'