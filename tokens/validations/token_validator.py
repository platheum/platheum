from rest_framework.response import Response
from rest_framework import status



def validate_tokens_input(func):
    """check provide key and refresh token from the request and make sure they are all provide and valid"""
    def dec(request):
        try:
            key = request.data['key']
            refresh_token = request.headers['Authorization']
            if refresh_token == '':
                return Response({'error':'refresh token is required'}, status.HTTP_400_BAD_REQUEST)
            elif key == '':
                return Response({'error':'token key is required'}, status.HTTP_400_BAD_REQUEST)
        except KeyError:
            return Response({'error':'key or refresh-token not included in the request'}, status.HTTP_400_BAD_REQUEST)
        else:
            return func(request, key, refresh_token)
    return dec