from .views import refreshToken
from django.urls import path

urlpatterns = [
    path('refresh-token/', refreshToken),
]
