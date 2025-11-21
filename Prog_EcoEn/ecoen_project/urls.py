# Prog_EcoEn/ecoen_project/urls.py
# ecoen_project/urls.py
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Admin
    path('admin/', admin.site.urls),

    # Allauth (login, logout, signup, social login)
    path('accounts/', include('allauth.urls')),
     
    # App principal
    path('', include('Prog_EcoEn.ecoen_app.urls')),   # tu app principal

    # Chatbot (solo si tienes una app llamada "chatbot")
    # Si no existe, elimina esta línea
    path('chatbot/', include('chatbot.urls')),
]

# Archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

