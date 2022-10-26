# notebook_search_api.py
''' Implementations for notebook search API

'''
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view

from notebooksearch import serializers
from notebooksearch import notebook_retrieval

from datetime import datetime

# from snotebook_search.serializers import NotebookSearchRequestSerializer
# from search_engine_app.notebook_search.serializers import NotebookSearchRequestLogSerializer

def str2datetime(timestamp:str): 
    ''' Transform a timestamp to datatime.datetime instance in UTC timezone. 
    '''
    return datetime.utcfromtimestamp(float(timestamp))


# -------------------------------- Working ----------------------------------
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def create_userprofile_api(request) -> Response: 
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
def notebook_search_api(request) -> Response: 
    ''' Return the notebook searching results to the client. 
    Args: 
        request: Received request from the client. 

    Returns: 
        Response(results): A list of notebook searching results. 
    '''

    try: 
        query_params = request.query_params
    except: 
        return Response({'Error': 'Request parameters are not given!'}, status = 400)
    # Validate request parameters
    param_serializer = serializers.NotebookSearchParamSerializer(data=request.query_params)
    if not param_serializer.is_valid(): 
        return Response(param_serializer.errors, status = 400)

    # Validate NotebookSearchLog data for `POST` method
    if request.method == 'POST': 
        log_serializer = serializers.NotebookSearchLogSerializer(data=request.data)
        if log_serializer.is_valid(): 
            log_serializer.save()  
        else: 
            return Response(log_serializer.errors, status = 400)

    # Retrieve notebooks from Elasticsearch dataserver
    index_name = "kaggle_notebooks"
    searcher = notebook_retrieval.NotebookRetriever(query_params, index_name)
    search_results = searcher.retrieve_notebooks()
    result_serializer = serializers.KaggleNotebookSearchResultSerializer(search_results)

    # Generate responses 
    if request.method == 'GET':     
        return Response(result_serializer.data, status = 200)
    elif request.method == 'POST': 
        return Response(result_serializer.data, status = 201)

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


