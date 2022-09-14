# notebook_search/apis.py
# Only used for handling REST APIs. 
from rest_framework.response import Response
from rest_framework.decorators import api_view

import json
@api_view(['GET'])
def welcome(request) -> Response: 
    ''' Return the welcome message to API connection. 
    Args: 
        request: Received request from the client. 

    Returns: 
        Response to the client.
    '''
    if request.method == 'GET':
        return Response({'name': 'notebook_search API', 'message': 'Congratulations! You have succefully received information from notebook_search API :)'})

@api_view(['GET'])
def api_test(request):
    if request.method == 'GET':
        print('GETTTTTTTTTTTT:', request.GET)
        return Response({'message': request.data})