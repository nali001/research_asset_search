# notebook_search/apis.py
# Only used for handling REST APIs. 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

from notebook_search.models import NotebookResult
from notebook_search.serializers import NotebookResultSerializer
from notebook_search import notebook_retrieval

import json

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


# from rest_framework.renderers import JSONRenderer
from django.http import JsonResponse

@api_view(['GET'])
@authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
def notebook_search(request) -> Response: 
    ''' Return the notebook searching results to the client. 
    Args: 
        request: Received request from the client. 

    Returns: 
        Response to the client.
    '''
    if request.method == 'GET':
        # Use NotebookResultSerializer to serialize one search result and 
        # Use json dumps to encode a list of serialized data
        # data = json.dumps([NotebookResultSerializer(msg[0]).data, NotebookResultSerializer(msg[0]).data])
        searcher = notebook_retrieval.Genericsearch(request)
        results = json.dumps(searcher.return_notebook_results())
        return Response(results)
        # return JsonResponse(results)

    