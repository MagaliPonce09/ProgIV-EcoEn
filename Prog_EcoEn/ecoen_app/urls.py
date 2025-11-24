# ecoen_app/urls.py
from django.urls import path, include
from . import views
from .views import CustomLoginView, CustomSignupView, chatbot_view
from .views import crear_preferencia

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),

    # Autenticación personalizada
    path("login/", CustomLoginView.as_view(), name="custom_login"),
    path("signup/", CustomSignupView.as_view(), name="custom_signup"),
    path("logout/", views.cerrar_sesion, name="custom_logout"),

    # Productos
    path("productos/", views.productos, name="productos"),
    path("producto/<int:id>/", views.producto_detalle, name="detalle_producto"),
    path("crear-producto/", views.crear_producto, name="crear_producto"),

    # Perfil
    path("perfil/", views.mi_perfil, name="mi_perfil"),
    path("perfil/editar/", views.editar_perfil, name="editar_perfil"),

    # Chatbot
    path("api/chatbot", chatbot_view, name="chatbot_view"),

    # Carrito y compras
    path("carrito/", views.carrito, name="carrito"),
    path("confirmar/<str:metodo>/", views.confirmar_pago, name="confirmar_pago"),
    path("resumen/", views.resumen_compra, name="resumen_compra"),

    # Opiniones
    path("opinion/", views.opinion_view, name="opinion"),

    # Allauth
    path("accounts/", include("allauth.urls")),

    #mercado pago
    
    path('crear-preferencia/', crear_preferencia, name='crear_preferencia'),

]
