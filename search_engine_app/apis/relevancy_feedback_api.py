# relevancy_feedback_api.py
''' Implementations for relevancy feedback API

'''
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes
from rest_framework.response import Response
from rest_framework.decorators import api_view

from notebooksearch import serializers


# The range for relevancy level
# Represented as 0-5(including 0 and 5) stars in the frontend
RELEVANCY_RANGE = 5

      
# -------------------------------- Working ----------------------------------
@api_view(['POST'])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def relevancy_feedback_api(request) -> Response: 
    ''' Store relevancy feedback from users  
    Args: 
        request: Received request from the client. 

    Returns: 
        Response(results): generated queries. 
    '''
    if request.method == 'POST': 
        # Validate the data using serializer
        request_serializer = serializers.RelevancyFeedbackLogSerializer(data=request.data)
        if request_serializer.is_valid():
            # Check the value range of `num_stars`
            num_stars = request_serializer.validated_data["num_stars"]
            if int(num_stars) in range(RELEVANCY_RANGE): 
                # ======= Save request.data to database =========
                request_serializer.save()
                return Response(request_serializer.data, status = 201)

        else: 
            return Response(request_serializer.errors, status = 400)
# -----------------------------------------------------------------------