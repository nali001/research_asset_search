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
### Main data models
`<user object>` 
```
{
    "user_id": user_id, 
}
```

`<query object>` 
```
{
    "query_text": query_text, 
}
```

`<notebook_result object>` 
```
{
    "notebook_id": notebook_id, 
    ... 
}
```

`<cell_content object>` 
```
{
    "cell_type": cell_type,
    "cell_text": cell_text,  
}
```


### A.1-A.2 [Notebook search session]
When clicking the search icon: 

client --> server \
`NotebookSearchRequest`
```
{
    "user": <user object>, 
    "timestamp": datetime, 
    "event": "notebook_search", 
    "query": <query object>,
}
```

server --> client \
`NotebookSearchResponse`
```
{
    "user": <user object>,  
    "event": "notebook_search", 
    "query": <query object>, 
    "notebook_results": [<notebook_result object>], 
}
```
server --> database \
`NotebookSearchLog` 
```
{
    "user": <user object>,  
    "event": "notebook_search", 
    "timestamp": timestamp, 
    "query": query, 
    "notebook_results": [<notebook_result object>], 
}
```


### B.1 [Query generation session]
When clicking the "Context-based search" button: 

client --> server \
`QueryGenerationRequest`
```
{
    "user": <user object>, 
    "event": "query_generation", 
    "cell_content": <cell object>, 
}
```

server --> client \
`QueryGenerationResponse`
```
{
    "user": <user object>, 
    "event": "query_generation", 
    "cell_content": <cell object>, 
    "generated_queries": [<query object>], 
}
```

### B.2-B.3 [Context-based search session]
When clicking the search icon:

client --> server \
`ContextSearchRequest`
```
{
    "user": <user object>, 
    "event": "context_based_search", 
    "cell_content": <cell object>, 
    "generated_queries": [<query object>], 
    "issued_query": <query object>, 
}
```

server --> client \
`ContextSearchResponse`
```
{
    "user": <user object>, 
    "event": "context_based_search", 
    "cell_content": <cell object>, 
    "generated_queries": [<query object>], 
    "issued_query": <query object>, 
    "notebook_results": [<notebook_result object>], 
}
```

server --> client \
`ContextSearchLog`
```
{
    "user": <user object>, 
    "event": "context_based_search", 
    "cell_content": <cell object>, 
    "generated_queries": [<query object>], 
    "issued_query": <query object>, 
    "notebook_results": [<notebook_result object>], 
}
```


### D.1-D.2 [relevancy annotation]
When clicking the stars: \
client --> server \
`RelevancyFeedbackRequest`
```
{
    "user": <user object>, 
    "event": "relevancy_feedback", 
    "query": <query object>, 
    "notebook": <notebook_result object>, 
    "num_stars": num_stars, 
}
```

server --> client \
`RelevancyFeedbackResponse`
```
{
    "user": <user object>, 
    "event": "relevancy_feedback", 
    "query": query, 
    "notebook": <notebook_result object>, 
    "num_stars": num_stars, 
    "success": True, 
}
```
If success is not True, then the client should send the data again. 

server --> database \
`RelevancyFeedbackLog`
```
{
    "user": <user object>, 
    "event": "relevancy_feedback", 
    "query": query, 
    "notebook": <notebook_result object>, 
    "num_stars": num_stars, 
}
```