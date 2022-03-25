from django.shortcuts import get_object_or_404, render
from numpy import block
from rest_framework.response import Response
from rest_framework.decorators import api_view
from users.models import User
from django.forms import ModelForm
from rest_framework import status
from blocks.models import Block

class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'country', 'password']








@api_view(['POST'])
def startWallet(request):
    form = UserForm(request.data)

    if form.is_valid():
        form.instance.set_password(form.cleaned_data['password'])
        form.save()
        # create a wallet for the user
    else:
        return Response({'errors': dict(form.errors)}, status.HTTP_406_NOT_ACCEPTABLE)

    return Response({'success':'signUp wallet completed'})