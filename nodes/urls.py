from django.urls import path, include
from .views import *

urlpatterns = [
    path('', home_page),
    path('blocks/', pending_blocks),
    path('mine/<int:bID>/', mine_block),
    path('<int:blockID>/', block_detail),
]

