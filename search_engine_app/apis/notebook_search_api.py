# notebook_search/apis.py
# Only used for handling REST APIs. 
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

from notebook_search import notebook_retrieval
from notebook_search import utils
from notebook_search import serializers
from rest_framework.response import Response
from rest_framework.decorators import api_view

from datetime import datetime

# from snotebook_search.serializers import NotebookSearchRequestSerializer
# from search_engine_app.notebook_search.serializers import NotebookSearchRequestLogSerializer

def str2datetime(timestamp:str): 
    ''' Transform a timestamp to datatime.datetime instance in UTC timezone. 
    '''
    return datetime.utcfromtimestamp(float(timestamp))



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



# @api_view(['POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def database_test(request) -> Response: 
#     ''' Return the welcome message to API connection. 
#     Args: 
#         request: Received request from the client. 

#     Returns: 
#         Response to the client.
#     '''
#     if request.method == 'POST':
#         return Response(request.data)


# @api_view(['GET'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def notebook_search(request) -> Response: 
#     ''' Return the notebook searching results to the client. 
#     Args: 
#         request: Received request from the client. 

#     Returns: 
#         Response(results): A list of notebook searching results. 
#     '''
#     if request.method == 'GET':
#         # Generate notebook search results for API endpoint. 
#         # Iterate the search results and for each result create a new models.NotebookResultSerializer object.
#         index_name = "kaggle_notebooks"
#         searcher = notebook_retrieval.Genericsearch(request, es, index_name)
#         searchResults = searcher.genericsearch()
#         results = []
#         for item in searchResults['results']: 
#             results.append(serializers.KaggleNotebookResultSerializer(item).data)
#             # results.append(serializers.GithubNotebookResultSerializer(item).data)
#         return Response(results) 
    

# @api_view(['GET', 'POST'])
# @authentication_classes([TokenAuthentication])
# @permission_classes([IsAuthenticated])
# def notebook_search_test(request) -> Response: 
#     ''' Return the notebook searching results to the client. 
#     Args: 
#         request: Received request from the client. 

#     Returns: 
#         Response(results): A list of notebook searching results. 
#     '''
#     if request.method == 'GET':
#         # Generate notebook search results for API endpoint. 
#         # Iterate the search results and for each result create a new models.NotebookResultSerializer object.
#         index_name = "kaggle_notebooks"
#         searcher = notebook_retrieval.Genericsearch(request, es, index_name)
#         searchResults = searcher.genericsearch()
#         results = []
#         for item in searchResults['results']: 
#             results.append(serializers.KaggleNotebookResultSerializer(item).data)
#             # results.append(serializers.GithubNotebookResultSerializer(item).data)
#         return Response(results) 
    
#     elif request.method == 'POST':
#         # print(f'REQUESTTTTTTTTTTTT: {request.data}')

#         # Validate the data using serializer
#         request_serializer = serializers.NotebookSearchRequestSerializer(data=request.data)
#         if request_serializer.is_valid(): 
#             request_serializer.save()
#             # Transform the request data to log data and save it into the database
#             request_data = request_serializer.data
#             request_data['timestamp'] = str2datetime(request_data['timestamp'])
#             return Response(request_data, status = 201)
#             # serializer.save()
#             # else: 
#             #     print('NNNNNNNNNOoooooooo')
#             #     return Response(request_data, status = 200) 
#         else: 
#             return Response(request_data, status = 400)

        
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_user(request) -> Response: 
    ''' Return the notebook searching results to the client. 
    Args: 
        request: Received request from the client. 

    Returns: 
        Response(results): A list of notebook searching results. 
    '''
    if request.method == 'POST':
        # print(f'REQUESTTTTTTTTTTTT: {request.data}')

        # Validate the data using serializer
        request_serializer = serializers.UserSerializer(data=request.data)
        if request_serializer.is_valid(): 
            request_serializer.save()
            # Transform the request data to log data and save it into the database
            request_data = request_serializer.data
            # request_data['timestamp'] = str2datetime(request_data['timestamp'])
            return Response(request_data, status = 201)
            # serializer.save()
            # else: 
            #     print('NNNNNNNNNOoooooooo')
            #     return Response(request_data, status = 200) 
        else: 
            return Response(request_serializer.errors, status = 400)




