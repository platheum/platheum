from django.contrib import admin
from django.urls import path, include
from .views import startWallet
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('tokens.urls')),
    path('start/', startWallet),
    path('wallet/', include('wallets.urls')),
    path('users/', include('users.urls')),
    path('nodes/', include('nodes.urls')),
   
]





if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
        urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
