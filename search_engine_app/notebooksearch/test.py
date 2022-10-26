# Add one more column
import pandas as pd
import os
path = './Kaggle Notebooks/es_kaggle_notebooks.csv'
notebooks = pd.read_csv(path)
notebooks["source"] = "Kaggle"
notebooks.to_csv(path, index=False)