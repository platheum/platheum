from tokens.models import Token
import jwt


# Response({'error': 'refresh token is Invalid'}, status.HTTP_400_BAD_REQUEST)

def authenticate(key: str, refresh_token: str):
    try:
        refresh_decoded_token = jwt.decode(refresh_token, "secret", algorithms=["HS256"])
    except Exception as e:
        return ''
    


    return Token.objects.filter(key=key, refresh_token=refresh_token, token_hash=refresh_decoded_token['keyHash']).first()
  