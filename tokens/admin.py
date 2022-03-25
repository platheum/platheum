from django.contrib import admin
from .models import Token, TokenBlackList
from django.http import HttpResponseRedirect


admin.site.site_header = 'PLATHEUM ADMIN'.capitalize()
@admin.register(TokenBlackList)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('date','token')
    def has_delete_permission(self, request, obj=None):
        return False

    def has_change_permission(self, request, obj=None):
        return False



@admin.register(Token)
class AuthorAdmin(admin.ModelAdmin):
    list_display = ('key', 'refresh_token')
    def has_add_permission(self, request, obj=None):
        return False
    def has_delete_permission(self, request, obj=None):
        return not request.user.id == 1

    def has_change_permission(self, request, obj=None):
        return False
    
    def get_readonly_fields(self, request, obj=None):

        if obj:
            return ['token_salt', 'key', 'refresh_token', 'token_hash', 'user']
        else:
            return []


