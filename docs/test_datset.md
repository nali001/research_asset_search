# Design for test dataset
What data can I collect? 
What so we do about these data? 

## User rating data
Ref to [MovieLens ml-latest-small](https://grouplens.org/datasets/movielens/)

Related tasks: 
- **Click-through-rate (CTR) prediction**: a special version of **recommender system** in which the goal is predicting whether or not a user is going to click on a recommended item.

### User-notebook interactions
| Variables     | Data type |
| ----------- | ----------- |
| User ID   | number        |
| Notebook ID      | number       |
| Rating | number 0-5 (scale 0.5) |
| Tag | text |
| Timestamp | time |


### Notebook profiles
| Variables     | Data type |
| ----------- | ----------- |
| Notebook ID      | number      |
| Title | text |
| Description | text |
| Git stars | number |
| Kaggle stars | number |
| Git link | URL |
| Kaggle link | URL |


### User profiles
| Variables     | Data type |
| ----------- | ----------- |
| User ID      | text       |
| Research interests | text |


## Query-document relevancy data
Ref to [TREC-robust-2004](https://trec.nist.gov/data/t13_robust.html)

Related tasks: 
- Ad hoc document retrieval

### Topics/Queries
| Variables     | Data type |
| ----------- | ----------- |
| qid   | number        |
| query      | text       |

### Relevancy judgements
| Variables     | Data type |
| ----------- | ----------- |
| qid   | number        |
| docno      | number       |
| relevancy | 0 to 5 |

Example



## Learn to rank
When ranking a notebook, note just relevancy will be considered, some other factors, such as the quality of the notebook (e.g., code reproducibility) are also of great importance. Thus we can utilize learn-to-rank framework to aggregate different ranking features into a final ranking. 

Ref to [LETOR 4.0]()

Related tasks: 
- Ad hoc document retrieval
