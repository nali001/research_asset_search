# System Design
## Frontend UI
### A. Notebook search
![Notebook search](images/notebook_search.png)

### B. Context-based search
![Context-based search](images/context_based_search.png)

### C. Result inspection
![Result inspection](images/result_inspection.png)

### D. Relevancy feedback
![Relevancy feedback](images/relevancy_feedback.png)

### E. Review history
![Review history](images/review_history.png)


-----------------------------------------------------------------------------------------------
## Data exchange between frontend and backend
### A.1-A.2 [current progress]
When clicking the search icon: 

client --> server
```
{
    'user_id': user_id, 
    'event': 'notebook_search', 
    'query': query,
}
```

server --> client
```
{
'event': 'notebook_search', 
'query': query, 
'search_results': search_results
}
```


### B.1 [next step]
When clicking the 'Context-based search' button: 

client --> server
```
{
'event': 'context_based_search', 
'cell_content': content
}
```

server --> client 
```
{
'event': 'context_based_search', 
'cell_content': content, 
'generated_queries': generated_queries
}
```

### B.2-B.3 [similar to A.1-A.2]
When clicking the search icon:

client --> server
```
{
'event': 'context_based_search', 
'generated_queries': generated_queries, 
'actual_query': actual_query
}
```

server --> client 
```
{
'event': 'context_based_search', 
'actual_query': actual_query, 
'search_results': search_results
}
```


### D.1-D.2 [relevancy annotation]
When clicking the stars: \
client --> server
```
{
    'event': 'relevancy_feedback', 
    'query': query, 
    'notebook_id': notebook_id, 
    'num_stars': num_stars
}
```

server --> client 
```
{
'event': 'relevancy_feedback', 
'query': query, 
'notebook_id': notebook_id, 
'num_stars': num_stars, 
'success': True
}
```