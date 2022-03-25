from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Token, TokenBlackList
import jwt
from rest_framework import status
from .serializers import TokenSerializer
from wallets.serializers import WalletSerializers
from users.serializers import UserSerializer
from transactions.serializers import TransactionSerializer
from .validations.token_validator import validate_tokens_input
from transactions.models import Transaction

@api_view(['PUT'])
@validate_tokens_input
def refreshToken(request, key, refresh_token):    
    token = Token.objects.filter(key=key).first()
    if token is None:
        return Response({'error':'Invalid Authentication Key'}, status.HTTP_404_NOT_FOUND)
        
    try:
        try:
            refresh_decoded_token = jwt.decode(refresh_token, "secret", algorithms=["HS256"])
        except jwt.exceptions.DecodeError:
            return Response({'error':'cannot decode. failed validation'}, status.HTTP_400_BAD_REQUEST)
    except jwt.exceptions.InvalidSignatureError:
        return Response({'error':'JWT Invalid Signature'}, status.HTTP_400_BAD_REQUEST)

    if not token.check_token_hash(refresh_decoded_token['keyHash']):
        return Response({'error': 'R-token is invalid'}, status.HTTP_400_BAD_REQUEST)
        
    TokenBlackList.objects.create(token=token.refresh_token)
    
    token.refresh_t()

    TSerializer = TokenSerializer(token, many=False)
    WSerializer = WalletSerializers(token.user.wallet, many=False)
    USerializer = UserSerializer(token.user, many=False)
    Tx1Serializer = TransactionSerializer(Transaction.objects.filter(sender=token.user.wallet.receive_key), many=True)
    Tx2Serializer = TransactionSerializer(Transaction.objects.filter(receiver=token.user.wallet.receive_key), many=True)

    return Response({'token':  TSerializer.data,
                        'wallet': {
                        'owner': USerializer.data,
                        'instance': WSerializer.data,
                        'transactions': {
                            'sended': Tx1Serializer.data,
                            'received': Tx2Serializer.data,
                        }
                    }}, status.HTTP_202_ACCEPTED)
