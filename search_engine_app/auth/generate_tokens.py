from rest_framework.authtoken.models import Token

if __name__ == '__main__': 
    token = Token.objects.create(user='aubergine')
    print(token.key)