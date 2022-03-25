

from transactions.models import Transaction
from django.db import models

from blocks.models import Block
from django.contrib.auth.hashers import  get_random_string
from utils.blocks import generateBlockStatement


def generate_salt(length=12):
    return get_random_string(length=length)

def getLastestBlock():
    return list(Block.objects.all())[-1]



class BlockChain(models.Model):
    chain = models.ManyToManyField(Block)

    @staticmethod
    def createCandidateBlock(transaction: Transaction):
        """for creating a canditate new instance of block

        Args:
            block (Block): the new block data
        """
        data:str=generateBlockStatement(
            amount=transaction.amount,
            sender=transaction.sender,
            receiver=transaction.receiver,
            date=transaction.time_stamp,
            message='this is testing statement'
        )

        Block.objects.create(
            hash=generate_salt(),
            tx_hash=transaction.hash,
            nonce=generate_salt(),
            added_to_bc=False,
            data=data,
            previous_hash=getLastestBlock().hash,
        )
        ...


  