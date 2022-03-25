from django.test import TransactionTestCase
from transactions.models import Transaction
from users.models import User
from blocks.models import Block
from .models import Wallet
from tokens.models import Token
from transactions.serializers import TransactionSerializer
from users.serializers import UserSerializer
from wallets.serializers import WalletSerializers
from transactions.serializers import TransactionSerializer

from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework import status


from tokens.validations.token_validator import validate_tokens_input
from .config.backend import authenticate
from decimal import *
from blockschain.models import BlockChain

@api_view(['POST'])
@validate_tokens_input
def Transfer(request, key: str, refresh_token:str, query: dict={}) -> Response:
    """
        AUTHENTICATE THE PROCCESS OF ACCESSING WALLET FOR PENDING
        TRANSACTION AND RECRUITMENT OF NEW CANDIDATE BLOCK

        authenticate user's tokens
        find and validate wallet
        authorize user and wallet
        -
        find and validate receiver's wallet
        sanitize and valid quered amount
       
        @query inputs:
            key | required. [request body]
            refresh-token | required. [request headers]

            private-key | required, [request body]
            payee-receive-key | required. [request body]
            paymentamount | required | required, [request body]

        
        create a pending transaction object and create an "orphan block" and then saved em

    """
    try:
        private_key = request.data['private_key']
        amount = request.data['amount']
        receiver_key = request.data['receiver_key']
    except Exception as e:

        return Response({'msg': f'[{e}] is required in transfer body'}, status.HTTP_400_BAD_REQUEST)


    # authenticate user

    token = authenticate(key, refresh_token)
    if token is None:
        return Response({'msg': 'Authentication failed. invalid tokens.'}, status.HTTP_400_BAD_REQUEST)
    elif token == '':
        return Response({'error': 'invalid signature provided.'}, status.HTTP_400_BAD_REQUEST)
    # ----- end --- #


    # make sure user is in token object
    if token.user is None:
        return Response({'error': 'user cannot be recovered.'}, status.HTTP_401_UNAUTHORIZED)



    # find wallet
    wallet = Wallet.objects.filter(private_key=private_key).first()
    if wallet == None:
        return Response({'msg': 'invalid wallet private key'}, status.HTTP_400_BAD_REQUEST)
    

    # authorize user with wallet
    try:
        if wallet != token.user.wallet:
            return Response({'msg': f'wallet dose"t belong to user:{token.user.hash}'})
    except User.wallet.RelatedObjectDoesNotExist:
        return Response({'msg': 'user dont owned a wallet'})
    # ---- end -----#




    # find receiver wallet 
    receiver_wallet = Wallet.objects.filter(receive_key=receiver_key).first()
    
    if receiver_wallet == None:
        return Response({'msg': 'receiver wallet not found'})

    if receiver_wallet == wallet:
        return Response({'msg': 'you cant send coins to your wallet'})


    
    # sanitizing amount
    try:
        query_amount = Decimal(amount)
    except InvalidOperation:
        return Response({'error': 'query amount is allowed to be only number'})
    except (ValueError, TypeError):
        return Response({'error': 'hmm, argument must be a string or a number, not list'})
        
    if query_amount == 0:
        return Response({'error': 'query amount must be greater than zero'})
    # ----- end ------ #



    # check balance sufficient
    if query_amount > wallet.balance:
        return Response({'msg': 'not enough coins'})


    # create transaction instance
    data={
        'query_amount': query_amount,
        'sender': wallet.receive_key,
        'receiver': receiver_key
    }
    PendingTransaction: Transaction = Transaction.initiateTransaction(data)
    BlockChain.createCandidateBlock(PendingTransaction)
   
 
    # create candidate block

    # print(PendingTransaction.getTxHashNodes())
   
    # return data

    TxSerializer  = TransactionSerializer(PendingTransaction, many=False)
    return Response(TxSerializer.data)
