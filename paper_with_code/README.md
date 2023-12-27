- [PapwerWithCode dataset](https://github.com/paperswithcode/paperswithcode-data)

- [Cleaned PapwerWithCode dataset with tasks label](https://huggingface.co/datasets/J0nasW/paperswithcode)

- [DataFinder](https://github.com/viswavi/datafinder)

## Prepare
- Get github access token from [github->settings->developer settings](https://github.com/settings/tokens)
- Save the token in the file .github_token in this folder

## Make the joint data between paper-to-code mapping and the datafinder labeled training set which includes the query, positive dataset, and negative datasets to the paper.

- We first use the provided labeled training set. For further process, we can use the [S2ORC](https://paperswithcode.com/dataset/s2orc) dataset. 

- Download the full text with the [SemanticScholar API](https://www.semanticscholar.org/product/api)
```bash
crawle_s2orc.py
```

Find the intersection between datafinder and PWC.
```bash
python crawle_datafinder_notebooks.py --papercode_mapfile datafinder_pwc_merged_paper_with_code.jsonl.gz --start 0 --end 10 --notebook_file github_notebook_file.0.10.jsonl --repo_search_results github_repo_file.0.10.jsonl  --github_token .github_token
```
- The output file: `datafinder_pwc_merged_paper_with_code.jsonl.gz`


## Crawle notebooks from github repos



