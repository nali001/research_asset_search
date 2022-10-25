# notebook_search_api.py
''' Implementations for context-based notebook search API

'''
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view

from notebooksearch import serializers
from notebooksearch import context_search
from apis import notebook_search_api



      
# -------------------------------- Working ----------------------------------
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def query_generation_api(request) -> Response: 
    ''' Generate queries for given cell contents 
    Args: 
        request: Received request from the client. 

    Returns: 
        Response(results): generated queries. 
    '''
    if request.method == 'POST': 
        # Validate the data using serializer
        request_serializer = serializers.QueryGenetationLogSerializer(data=request.data)
        if request_serializer.is_valid():
            # ======= Save request.data to database =========
            request_serializer.save()
            pass
        else: 
            return Response(request_serializer.errors, status = 400)
        
        # Generate queries based on the cell contents
        request_data = request_serializer.data
        cell_contents = request_data["cell_contents"]

        generator = context_search.QueryGenerator(cell_contents)
        generated_queries = generator.generate_queries()


        # Merge results from two serializers
        results = {**request_data, **{"generated_queries": generated_queries}}
        print(f'GENERATION RESUUUUUULTS: \n\n{results}\n\n')
        
        # Serialize the response
        result_serializer = serializers.QueryGenerationResultSerializer(results)
        return Response(result_serializer.data, status = 200)
# -----------------------------------------------------------------------
   
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def context_search_api(request) -> Response: 
    ''' Contexted based search 
    
    It receives input as cell contents and return notebook search results. 
    The whole functionality includes two parts: query generation and notebook search
    Args: 
        request: Received request from the client. 

    Returns: 
        Response(results): context_based notebook search results
    '''
    if request.method == 'POST': 
        # Validate the data using serializer
        request_serializer = serializers.ContextSearchLogSerializer(data=request.data)
        if request_serializer.is_valid(): 
            # ======= Save request.data to database =========
            request_serializer.save()
            pass
        else: 
            return Response(request_serializer.errors, status = 400)
        
        # Strip the request.data and use remaining for notebook search
        request_data = request_serializer.data
        request_data["event"] = "notebook_search"
        request_data.pop("cell_contents")
        request_data.pop("generated_queries")
        request.data = request_data

        print(f'DAAAAAATTTTAAAAAAA: {request.data}\n')
        search_results = notebook_search_api.notebook_search(request)

        # Merge results from two serializers
        results = {**request_serializer.data, **{"search_results": search_results}}
        
        # Serialize the response
        result_serializer = serializers.KaggleContextSearchResultSerializer(results)
        return Response(result_serializer.data, status = 201)