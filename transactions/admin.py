from django.contrib import admin
from .models import Transaction
from django.utils.safestring import mark_safe


@admin.register(Transaction)
class AuthorAdmin(admin.ModelAdmin):
     list_display = ('amount', 'txType', 'status_','completed', 'is_valid', 'time_stamp',)
    #  list_filter = ('status',)


    
     def has_add_permission(self, request, obj=None):
        return False
     def has_delete_permission(self, request, obj=None):
        return not request.user.id == 1

   #   def has_change_permission(self, request, obj=None):
   #      return False


     def status_(self, obj):
        bg = '#F2C133' if obj.status == '100' else 'green' 
        return mark_safe(f'<b style="background: {bg}; color: #fff; padding: 3px 10px; border-radius: 10px">{obj.status}</b>')

     def is_valid(self, obj):
        bg = 'green' if obj.is_valid else 'red' 
        return mark_safe(f'<b style="color: {bg}; padding: 3px 10px; border-radius: 10px">{obj.is_valid}</b>')


    

     def get_readonly_fields(self, request, obj=None):

        if obj:
            return [  'sender', 'txType', 'receiver', 'hash', 'status', 'completed', 'has_block']
        else:
            return []

