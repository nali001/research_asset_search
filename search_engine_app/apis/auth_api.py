from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import authentication_classes
from rest_framework.decorators import permission_classes

@api_view(['GET'])
def initialize_app(request) -> Response: 
    ''' Initialize the application by creating superuser `admin`

    username: admin
    Email: admin@notebooksearch.com
    Password: notebooksearch2022
    '''
    # Create superuser `admin`
    try: 
        user = User.objects.get(username='admin')
    except: 
        user = User.objects.create_superuser('admin', 'admin@notebooksearch.com', 'notebooksearch2022') 
    return Response({
        'Activity': f'Created User `{user.username}`',
    })


@api_view(['GET'])
def obatain_api_token(request) -> Response: 
    ''' Show the token for user `aubergine` which will be used for token authentication of some APIs
    '''
    # Create user `aubergine` if not exists
    try: 
        user = User.objects.get(username='aubergine')
    except: 
        user = User.objects.create_user('aubergine', 'aubergine@notebooksearch.com', 'notebooksearch2022') 
    token, created = Token.objects.get_or_create(user=user)
    return Response({
        'Token': token.key,
    })

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
        msg = {'name': 'Search engine API', 'message': 'Congratulations! You have be authenticated by the API :)'}
        return Response(msg)


