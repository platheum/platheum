from django.contrib import admin
from .models import Wallet

@admin.register(Wallet)
class AuthorAdmin(admin.ModelAdmin):
     list_display = ('id', 'receive_key', 'owner', 'balance')
     def has_add_permission(self, request, obj=None):
        return False
     def has_delete_permission(self, request, obj=None):
        return not request.user.id == 1

   #   def has_change_permission(self, request, obj=None):
   #      return False
     def get_readonly_fields(self, request, obj=None):

        if obj:
            return [ 'owner', 'balance_in_ngn', 'public_key', 'private_key', 'receive_key']
        else:
            return []