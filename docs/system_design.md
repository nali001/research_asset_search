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
`<ClientUser>` 
```
{
	"id": id, 
    "client_id": client_id, 
}
```

`<GeneratedQuery object>` 
```
{
	"id": id, 
    "method": generation_method, 
    "queries": [query_text], 
}
```

`<KaggleNotebook object>` 
```
{
	"id": id, 
	"id": id, 
    "name": name, 
    "html_url": html_url, 
    "description": description, 
    "kaggle_id": kaggle_id,
    "file_name": file_name, 
}
```

`<CellContent object>` 
```
{
	"id": id, 
    "cell_type": cell_type,
    "cell_content": cell_content,  
}
```


### A.1-A.2 [Notebook search session]
When clicking the search icon: 

client --> server \
`NotebookSearchLogSerializer`
```
{
	"id": id, 
    "client_id": client_id, 
    "timestamp": timestamp, 
    "event": "notebook_search", 
    "query": query,
}
```

server --> client \
`NotebookSearchResultSerializer`
```
{
	"id": id, 
    "query" = query
    "facets" = facets
    "num_hits" = num_hits
    "num_pages" = num_pages
    "current_page" = current_page
    "results": [<KaggleNotebook object>], 
}
```
server --> database \
`NotebookSearchLogSerializer`
```
{
	"id": id, 
    "client_id": client_id, 
    "timestamp": timestamp, 
    "event": "notebook_search", 
    "query": query,
}
```


### B.1 [Query generation session]
When clicking the "Context-based search" button: 

client --> server \
`QueryGenerationLogSerializer`
```
{
	"id": id, 
    "client_id": client_id, 
    "timestamp": timestamp, 
    "event": "query_generation", 
    "cell_contents": [<CellContent object>]
}
```

server --> client \
`QueryGenerationResultSerializer`
```
{
	"id": id, 
    "client_id": client_id, 
    "timestamp": timestamp, 
    "event": "query_generation", 
    "cell_contents": [<CellContent object>], 
    "generated_queries": [<GeneratedQuery object>], 
}
```

server --> database \
`QueryGenerationLogSerializer`
```
{
	"id": id, 
    "client_id": client_id, 
    "timestamp": timestamp, 
    "event": "query_generation", 
    "cell_contents": [<CellContent object>]
}
```

### B.2-B.3 [Context-based search session]
When clicking the search icon:

client --> server \
`ContextSearchLogSerializer`
```
{
	"id": id, 
    "client_id": client_id, 
    "timestamp": timestamp, 
    "event": "context_search", 
    "query": query, 
    "cell_contents": [<CellContent object>]
    "generated_queries": [<GeneratedQuery object>], 
}
```

server --> client \
`KaggleContextSearchResultSerializer`
```
{
	"id": id, 
    "client_id": client_id, 
    "timestamp": timestamp, 
    "event": "context_search", 
    "query": query, 
    "cell_contents": [<CellContent object>], 
    "generated_queries": [<GeneratedQuery object>], 
    "search_results": [<NotebookSearchResult object>], 
}
```

server --> client \
`ContextSearchLogSerializer`
```
{
	"id": id, 
    "client_id": client_id, 
    "timestamp": timestamp, 
    "event": "context_search", 
    "cell_contents": [<CellContent object>]
    "generation_results": [<GeneratedQuery object>], 
    "query": query
}
```


### D.1-D.2 [relevancy annotation]
When clicking the stars: \
client --> server \
`RelevancyFeedbackRequest`
```
{
	"id": id, 
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
	"id": id, 
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
	"id": id, 
    "user": <user object>, 
    "event": "relevancy_feedback", 
    "query": query, 
    "notebook": <notebook_result object>, 
    "num_stars": num_stars, 
}
```