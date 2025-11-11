from django.contrib import admin
from .models import Producto, Perfil, Opinion, Compra, Puntuacion

admin.site.register(Producto)
admin.site.register(Perfil)
admin.site.register(Opinion)
admin.site.register(Compra)
admin.site.register(Puntuacion)
