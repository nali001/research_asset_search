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


      
# -------------------------------- Working ----------------------------------
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def query_generation(request) -> Response: 
    ''' 
    Args: 
        request: Received request from the client. 

    Returns: 
        Response(results):  
    '''
    if request.method == 'POST': 
        # Validate the data using serializer
        request_serializer = serializers.QueryGenetationLogSerializer(data=request.data)
        if request_serializer.is_valid(): 
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
        results = {**request_data, **{"generation_results": generated_queries}}
        
        # Serialize the response
        result_serializer = serializers.QueryGenerationResultSerializer(results)
        return Response(result_serializer.data, status = 200)
# -----------------------------------------------------------------------
   