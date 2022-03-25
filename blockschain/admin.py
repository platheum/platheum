from django.contrib import admin
from .models import BlockChain

# Register your models here.

@admin.register(BlockChain)
class AuthorAdmin(admin.ModelAdmin):
    ...