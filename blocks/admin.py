from django.contrib import admin
from .models import Block

# Register your models here.

@admin.register(Block)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('index', 'time_stamp','added_to_bc',)
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False


    def get_readonly_fields(self, request, obj=None):

        if obj:
            return [ 'txList', 'txHashList',]
        else:
            return []