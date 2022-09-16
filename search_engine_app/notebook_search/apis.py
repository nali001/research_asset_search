# notebook_search/apis.py
# Only used for handling REST APIs. 
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes


@api_view(['GET'])
@authentication_classes([SessionAuthentication, BasicAuthentication])
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
        return Response(content)

@api_view(['GET'])
def api_test(request):
    if request.method == 'GET':
        print('GETTTTTTTTTTTT:', request.GET)
        return Response({'message': request.data})