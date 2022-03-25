import re
from django.shortcuts import get_object_or_404, render
from blocks.models import Block
from wallets.models import Wallet
from transactions.models import Transaction

def home_page(request):
    return render(request, 'nodes/pageindex.html', {})


def mine_block(request, bID):
    print(request.user)
    block = get_object_or_404(Block, index=bID)
    block.added_to_bc = True 
    block.save()
    Transaction.objects.filter(hash=block.transaction).update(completed=True, status=300)

    Wallet.objects.filter(receive_key=block.get_transaction.receiver).update(balance=block.get_transaction.payee.balance+1020)
    return render(request,'nodes/res.html', {})

def pending_blocks(request):
    blocks = Block.objects.filter(added_to_bc=False)
    return render(request,'nodes/index.html', {'blocks': list(blocks)})


def block_detail(request, blockID):
    block = get_object_or_404(Block, index=blockID)
    # print(tx)
    print(block.transaction)
    return render(request,'nodes/details.html', {'block': block})