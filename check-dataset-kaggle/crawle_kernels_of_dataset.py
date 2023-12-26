import os, glob, sys
import numpy as np
import json
from tqdm import tqdm
import re
from time import sleep
from kaggle.api.kaggle_api_extended import KaggleApi
import argparse


api = KaggleApi()
api.authenticate()

parser = argparse.ArgumentParser()
parser.add_argument('--data_folder', type=str, default='../../data/dataset/Kaggle')
parser.add_argument('--num_segments', type=int, default=10)
parser.add_argument('--segment_id', type=int, default=0)
args = parser.parse_args()

datasets = glob.glob(f'{args.data_folder}/PWC/*.json')

print(f"Total number of datasets: {len(datasets)}")

dataset_kernel_ref_map_file = open(f'{args.data_folder}/dataset_kernel_ref_map-{args.segment_id}.jsonl', 'w')

start = len(datasets)//args.num_segments*args.segment_id + 3000
end = len(datasets)//args.num_segments*(args.segment_id+1)
datasets = datasets[start:end]
for dataset_path in tqdm(datasets, total=len(datasets)):
    dataset = json.load(open(dataset_path))
    kernel_refs = api.kernels_list(dataset=dataset['ref'])
    dataset_kernel_ref_map_file.write(json.dumps({'dataset': dataset['ref'], 'kernel_refs':[kernel.ref for kernel in kernel_refs]}, ensure_ascii=False)+'\n')
    sleep(np.random.random()/3)
    
dataset_kernel_ref_map_file.close()
