from django.contrib import admin
from .models import User
from django import forms

# Register your models here.


@admin.register(User)
class AuthorAdmin(admin.ModelAdmin):
    fields = ('first_name', 'last_name', 'email', 'phone_number','password', 'hash')

    def save_model(self, request, obj, form, change):
        if not change:
            obj.set_password(obj.password)
        super(AuthorAdmin, self).save_model(request, obj, form, change)


    def get_readonly_fields(self, request, obj=None):
        if obj:
            return ['password', 'hash']
        else:
            return []
