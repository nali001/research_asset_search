# notebook_search/apis.py
# Only used for handling REST APIs. 
import re
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

from notebooksearch import genericsearch
from notebooksearch import notebook_retrieval

from notebooksearch import utils
from notebooksearch import serializers
from notebooksearch import models
from rest_framework.response import Response
from rest_framework.decorators import api_view

from datetime import datetime

from notebooksearch import notebook_retrieval

# from snotebook_search.serializers import NotebookSearchRequestSerializer
# from search_engine_app.notebook_search.serializers import NotebookSearchRequestLogSerializer

def str2datetime(timestamp:str): 
    ''' Transform a timestamp to datatime.datetime instance in UTC timezone. 
    '''
    return datetime.utcfromtimestamp(float(timestamp))


# # Create Elasticsearch client
# es = utils.create_es_client()

# -------------------------------- Working ----------------------------------
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
    if request.method == 'GET':
        msg = {'name': 'notebook_search API', 'message': 'Congratulations! You have succefully received information from notebook_search API :)'}
        return Response(msg)



@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_userprofile(request) -> Response: 
    ''' Create a user profile. 
    Args: 
        request: Received request from the client. 

    Returns: 
        user's request. 
    '''
    if request.method == 'POST':
        print(f'REQUESTTTTTTTTTTTT: {request.data}')

        # Validate the data using serializer
        request_serializer = serializers.UserProfileSerializer(data=request.data)
        if request_serializer.is_valid(): 
            request_serializer.save()
            # Transform the request data to log data and save it into the database
            request_data = request_serializer.data
            return Response(request_data, status = 201)
        else: 
            return Response(request_serializer.errors, status = 400)

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def notebook_search(request) -> Response: 
    ''' Return the notebook searching results to the client. 
    Args: 
        request: Received request from the client. 

    Returns: 
        Response(results): A list of notebook searching results. 
    '''
    # Retrieve notebooks from Elasticsearch
    query_data = request.query_params
    index_name = "kaggle_notebooks"
    searcher = notebook_retrieval.NotebookRetriever(query_data, index_name)
    search_results = searcher.retrieve_notebooks()

    # Serialize search results 
    result_serializer = serializers.KaggleNotebookSearchResultSerializer(search_results)

    if request.method == 'GET':     
        return Response(result_serializer.data, status = 200)
    
    elif request.method == 'POST': 
        # Validate the data using serializer
        request_serializer = serializers.NotebookSearchLogSerializer(data=request.data)
        if request_serializer.is_valid(): 
            request_serializer.save()
            return Response(result_serializer.data, status = 201)
        else: 
            return Response(result_serializer.data, status = 400)

# -----------------------------------------------------------------------

@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def test(request) -> Response: 
    ''' Return the notebook searching results to the client. 
    Args: 
        request: Received request from the client. 

    Returns: 
        Response(results): A list of notebook searching results. 
    '''
    def process_post_request(request): 
        ''' Process both `GET` and `POST` methods for notebook search 
        '''
        # Extract POST data
        try: 
            request_data = request.data
        except: 
            request_data = {}
        
        # Extract params for both `GET` and `POST`
        try: 
            request_params = request.query_params
        except: 
            request_params = {}
        
        # Combine request data and params
        request_data.update(request_params)
        
        query_data = {
            'query': '', 
            'page': 0, 
            'filter': '', 
            'facet': '', 
        }
        for key in request_data.keys(): 
            try: 
                val = request_data[key]
                query_data[key] = val
            except: 
                continue
        return query_data
    if request.method == 'GET':
        # Retrieve notebooks from Elasticsearch
        index_name = "kaggle_notebooks"
        query_data = request.query_params
        searcher = notebook_retrieval.NotebookRetrieval(query_data, index_name)
        search_results = searcher.retrieve_notebooks()

        # Serializing results and generate responses
        serializer = serializers.KaggleNotebookSearchResultSerializer(search_results)   
        return Response(serializer.data)

    if request.method == 'POST': 
        pass
    



# @api_view(['GET', 'POST'])
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
#         # Retrieve notebooks from Elasticsearch
#         query_data = request.query_params
#         index_name = "kaggle_notebooks"
#         searcher = notebook_retrieval.NotebookRetrieval(query_data, index_name)
#         search_results = searcher.retrieve_notebooks()

#         # Serialize search results 
#         serializer = serializers.KaggleNotebookSearchResultSerializer(search_results)   
#         return Response(serializer.data)
    
        
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
#         else: 
#             return Response(request_data, status = 400)
    
#     def process_requests(self): 
#         ''' Process both `GET` and `POST` methods for notebook search 
#         '''
#         # Extract POST data
#         try: 
#             request_data = self.request.data
#         except: 
#             request_data = {}
        
#         # Extract params for both `GET` and `POST`
#         try: 
#             request_params = self.request.query_params
#         except: 
#             request_params = {}
        
#         # Combine request data and params
#         request_data.update(request_params)
        
#         query_data = {
#             'query': '', 
#             'page': 0, 
#             'filter': '', 
#             'facet': '', 
#         }
#         for key in request_data.keys(): 
#             try: 
#                 val = request_data[key]
#                 query_data[key] = val
#             except: 
#                 continue
#         return query_data


