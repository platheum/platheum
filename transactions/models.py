from django.db import models
from users.models import User
from django.forms.models import model_to_dict

from wallets.models import Wallet
from .constants import *
from libs.cipher.semetrics import Cipher
from hashlib import sha256

class Transaction(models.Model):
    hash = models.TextField()
    amount = models.DecimalField(decimal_places=7, max_digits=12,default=0.0)
    txType = models.IntegerField(choices=txTypes, null=False)
    time_stamp = models.DateTimeField(auto_now_add=True)
    has_block = models.BooleanField(default=False)
    signature = models.TextField()
    status = models.CharField(max_length=200,
            choices=transaction_status,
            default='invalid',
            help_text='Specify the transaction stage'
    )
    sender = models.CharField(max_length=200, unique=False, help_text='The user hash:id who sends the coins')
    receiver = models.CharField(max_length=200,unique=False, help_text='The wallet receive address who receive the funds')
    time_stamp = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False, help_text='shows if the transaction is completed')
    
    @staticmethod
    def getTxHashNodes()-> list:
        result = [tx.hash for tx in list(Transaction.objects.all())]
        return result

    @staticmethod
    def initiateTransaction(data):
        transaction = Transaction.objects.create(
            amount=data['query_amount'],
            sender=data['sender'],
            receiver=data['receiver'],
            status=100,
            txType=211
        )
        cipher = Cipher(transaction)
        hasher = sha256()
        signature = cipher.encrypt()
        transaction.signature = signature
        hasher.update(bytes(signature, encoding='utf8'))

        transaction.hash = hasher.hexdigest()
        transaction.save()
        return transaction


    @property
    def payer(self):
        return Wallet.objects.filter(receive_key=self.sender).first()

    @property
    def payee(self):
        return Wallet.objects.filter(receive_key=self.receiver).first()


    @property
    def is_valid(self) -> bool:
        from libs.cipher.semetrics import Cipher
        cipher = Cipher(self)
        print(self.data)
        result = cipher.verify_signature(self.data)
        return result

    @property
    def data(self)-> str:
        instance = model_to_dict(Transaction.objects.filter(id=self.id).first(), exclude=['id', 'has_block', 'status', 'verified', 'hash', 'signature', 'status', 'completed'])
        return f'{instance}'    
    
   


    def __str__(self)->str:
        # return  f"{self.sender[:10]}.. TRANSFERRED {self.amount} COINS TO {self.receiver[:10]}.."
        return  f"{self.id}"