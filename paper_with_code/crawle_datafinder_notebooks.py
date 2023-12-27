import pandas as pd
import requests
import re
import json
import random
import time
import base64
import retry
import tqdm
import backoff
import argparse


parser = argparse.ArgumentParser()
parser.add_argument('--papercode_mapfile', type=str, default="paperswithcode-data/links-between-papers-and-code.json.gz")
parser.add_argument('--github_token', type=str, default=".github_token")
parser.add_argument('--repo_search_results', type=str, default="repo_search_results.jsonl")
parser.add_argument('--failed_repo', type=str, default="failed_repo.txt")
parser.add_argument('--failed_nb', type=str, default="failed_notebook.txt")
parser.add_argument('--notebook_file', type=str, default="notebook_file.jsonl")
parser.add_argument('--start', type=int, default=0)
parser.add_argument('--end', type=int, default=None)

args = parser.parse_args()


@backoff.on_exception(backoff.expo, Exception, max_tries=10, jitter=backoff.full_jitter)
def get_github_repo_ipynb(owner, repo, header):
    api_url = f'https://api.github.com/search/code?q=extension:ipynb+repo:{owner}/{repo}'
    response = requests.get(api_url, headers=header)
    if response.status_code != 200:
        print('retry', api_url)
        raise Exception(f"Error {response.status_code} for {api_url}")
    results = response.json()
    if 'items' not in results or 'message' in results:
        raise Exception(f"Error {response.status_code} for {api_url}")
    return results


# @retry.retry(tries=10, delay=3, backoff=2)
@backoff.on_exception(backoff.expo, [Exception], max_tries=10, jitter=backoff.full_jitter)
def get_github_file_content(url, header):
    response = requests.get(url, headers=header)                   
    data = response.json()
    if response.status_code != 200:
        print('retry', url)
        raise Exception(f"Error {response.status_code} for {url}")
    if 'content' not in data or 'message' in response.json():
        raise Exception(f"Error {response.status_code} for {url}")
    
    content = base64.b64decode(data['content']).decode('utf-8')    
    return content


papers_code_links = pd.read_json(args.papercode_mapfile, lines=True)
repo_urls = papers_code_links.repo_url.unique()
token = open(args.github_token, "r").read().strip()

print(token)

request_header = {
  "Accept": "application/vnd.github+json",
  "Authorization": f"Bearer {token}",
  "X-GitHub-Api-Version": "2022-11-28"
}


patern = ".*github.com/(.*)/(.*)"

repo_search_results = open(args.repo_search_results, "w") #  "repo_search_results.jsonl", "w")
failed_repo = open(args.failed_repo, "w")   #  "filed_repo.txt", "w")
failed_nb = open(args.failed_nb, "w") # "filed_notebook.txt", "w")
notebook_file = open(args.notebook_file, "w") # "notebook_file.jsonl", "w")

repo_urls = repo_urls[args.start:args.end]
for idx, repo_url in enumerate(tqdm.tqdm(repo_urls, total=len(repo_urls))):
    g = re.search(patern, repo_url)
    if g is not None:
        owner = g.group(1)
        repo = g.group(2)
        try:
            nb_items = get_github_repo_ipynb(owner, repo, request_header)   
        except:
            failed_repo.write(f"repo_url\n")
            continue
        repo_search_results.write(json.dumps(nb_items)+"\n")
        for item in nb_items['items']:
            time.sleep(1+random.random())
            metadata = {
                'owner': owner,
                'repo': repo,
                'repo_url': repo_url,
                'name': item['name'],
                'path': item['path'],
                'sha': item['sha']
            }
            try:
                data = get_github_file_content(item['url'], request_header)
            except Exception as e:
                print(e)
                failed_nb.write(f"{item['url']}\n")
                continue
            nb_info = {
                'metadata': metadata,
                'notebook': data
            }
            notebook_file.write(json.dumps(nb_info)+"\n")
failed_nb.close()
failed_repo.close()
notebook_file.close()
repo_search_results.close()