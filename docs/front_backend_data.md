# Fontend-backend data communitation
With Django framework, there are two means of data transfer between frontend and backend. 

### Web page
In the `views` version, the backend sends a `dict` to templates HTML. 
And the HTML access data directly. For example, 
```
% views.py

def data_view(request): 
    data = ...
    returned_data = {"result": data}
    return render(request, 'hello.html', returned_data)

% templates/hello.html
<script> const {{ result | safe }} </script>
```

### REST API
In the `api` version, the backend sends a `serialized json` object to clients. For example, 
```
% apis/notebook_search_api.py

def notebook_search_api(request) -> Response: 
    ...
    search_results = searcher.retrieve_notebooks()
    result_serializer = serializers.KaggleNotebookSearchResultSerializer(search_results)

    # Generate responses 
    if request.method == 'GET':     
        return Response(result_serializer.data, status = 200)
    elif request.method == 'POST': 
        return Response(result_serializer.data, status = 201)
```