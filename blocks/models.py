from django.db import models
from vine import transform
from transactions.models import Transaction


""""""

class OrphanBlock(models.Model):
    transaction = models.TextField()
    date = models.DateTimeField(auto_now=True)

class Block(models.Model):
    index = models.AutoField(primary_key=True)
    time_stamp = models.DateTimeField(auto_now=True)
    hash = models.CharField(max_length=255, blank=True)
    tx_hash = models.TextField()
    nonce = models.CharField(max_length=255, default=0, blank=True)
    data = models.TextField(blank=True, max_length=255)
    previous_hash = models.CharField(max_length=255)
    added_to_bc = models.BooleanField(default=False)
    
    @property
    def transaction(self):
        return Transaction.objects.filter(hash=self.tx_hash).first()


      
    @property
    def txList(self):
        return list(Transaction.objects.all())[0:self.transaction.id]

    @property
    def txHashList(self):
        return [tx.hash for tx in self.txList]

    def __str__(self) -> str:
        print(self.txList)
        return f'Block({self.index})'



    def is_valid(self):
        return True
  