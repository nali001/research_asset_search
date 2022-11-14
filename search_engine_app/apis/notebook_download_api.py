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
from notebooksearch import notebook_downloading

from datetime import datetime

# from snotebook_search.serializers import NotebookSearchRequestSerializer
# from search_engine_app.notebook_search.serializers import NotebookSearchRequestLogSerializer

def str2datetime(timestamp:str): 
    ''' Transform a timestamp to datatime.datetime instance in UTC timezone. 
    '''
    return datetime.utcfromtimestamp(float(timestamp))


# -------------------------------- Working ----------------------------------

# -----------------------------------------------------------------------
@api_view(['GET', 'POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def notebook_download_api(request) -> Response: 
    ''' Download the notebook for client. 

    Either retrieve from the database or download from Kaggle. 

    Args: 
        request: Received request from the client. 

    Returns: 
        Response(results): Notebook source file along with other meta info. 
    '''

    try: 
        query_params = request.query_params
    except: 
        return Response({'Error': 'Request parameters are not given!'}, status = 400)
    # Validate request parameters
    param_serializer = serializers.NotebookDownloadParamSerializer(data=request.query_params)
    if not param_serializer.is_valid(): 
        return Response(param_serializer.errors, status = 400)

    # Validate NotebookSearchLog data for `POST` method
    if request.method == 'POST': 
        log_serializer = serializers.NotebookDownloadSerializer(data=request.data)
        if log_serializer.is_valid(): 
            pass
            # log_serializer.save()  
        else: 
            return Response(log_serializer.errors, status = 400)

    # Retrieve notebooks from Elasticsearch dataserver
    docid = query_params['docid']
    downloader = notebook_downloading.NotebookDownloader()
    download_result = downloader.get_notebook_by_docid(docid)
    result_serializer = serializers.NotebookDownloadResultSerializer(download_result)

    # Generate responses 
    if request.method == 'GET':     
        return Response(result_serializer.data, status = 200)
    elif request.method == 'POST': 
        return Response(result_serializer.data, status = 201)


