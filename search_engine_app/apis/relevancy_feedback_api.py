# notebook_search/apis.py
# Only used for handling REST APIs. 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

from notebooksearch import notebook_retrieval
from notebooksearch import utils
from notebooksearch import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view


# Create Elasticsearch client
es = utils.create_es_client()

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def welcome(request) -> Response: 
    ''' Return the welcome message to API connection. 
    Args: 
        request: Received request from the client. 

    Returns: 
        Response to the client.
    '''
    content = {
        'user': str(request.user),  # `django.contrib.auth.User` instance.
        'auth': str(request.auth),  # None
    }
    if request.method == 'GET':
        msg = {'name': 'notebook_search API', 'message': 'Congratulations! You have succefully received information from notebook_search API :)'}
        return Response(msg)



@api_view(['GET'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def notebook_search(request) -> Response: 
    ''' Return the notebook searching results to the client. 
    Args: 
        request: Received request from the client. 

    Returns: 
        Response(results): A list of notebook searching results. 
    '''
    if request.method == 'GET':
        # Generate notebook search results for API endpoint. 
        # Iterate the search results and for each result create a new models.NotebookResultSerializer object.
        index_name = "kaggle_notebooks"
        searcher = notebook_retrieval.Genericsearch(request, es, index_name)
        searchResults = searcher.genericsearch()
        results = []
        for item in searchResults['results']: 
            results.append(serializers.KaggleNotebookResultSerializer(item).data)
            # results.append(serializers.GithubNotebookResultSerializer(item).data)
        return Response(results) 
    