# Prog_EcoEn/ecoen_project/urls.py

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Allauth (login, logout, signup, social login)
    path('accounts/', include('allauth.urls')),
    
    # Apps propias
    path('', include('Prog_EcoEn.ecoen_app.urls')),   # tu app principal
    path('chatbot/', include('chatbot.urls')),  # tu chatbot si tiene urls propias
    ]
# Archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL,
                          document_root=settings.STATIC_ROOT)
