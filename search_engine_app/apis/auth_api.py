# from django.contrib.auth.models import User
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['GET'])
def obatain_api_token(request) -> Response: 
    ''' Show the token for user `aubergine` which will be used for token authentication of some APIs
    '''
    try: 
        user = User.objects.get(username='aubergine')
    except: 
        user = User.objects.create_user('aubergine', 'aubergine@notebooksearch.com', 'notebooksearch2022') 
    token, created = Token.objects.get_or_create(user=user)
    return Response({
        'Token': token.key,
    })
