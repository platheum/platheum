from django.test import TestCase
from .models import Transaction

class TransactionTestCase(TestCase):
 

    def test_tx_hash_gen(self):
       print(Transaction.objects.count())
       print(Transaction.getTxHashNodes())