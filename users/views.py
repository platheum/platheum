from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import User
from django.contrib.auth import authenticate
from rest_framework import status
from tokens.models import Token

def validate_login_input(func):
    def dec(request):
        email = request.data['email']
        password = request.data['password']
        # valid
        if email.strip() == '' or password.strip() == '':
            return Response({'error':'username or password not provided'})
        user = authenticate(email=email, password=password)
        return func(request, user)

    return dec


@api_view(['POST'])
@validate_login_input
def Login(request, user) -> Response:
    """
        authenticate with given :email and password
        and response a tokens
    """
    if user is None:
        return Response({'error': 'wrong credentials provided'}, status.HTTP_401_UNAUTHORIZED)
    

    # just know that auth_token can be None
    token = user.auth_token
    token.refresh_t()

    # print(token)
    return Response({'refresh_token': token.refresh_token, 'key': token.key})
    