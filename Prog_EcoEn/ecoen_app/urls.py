from django.urls import path, include
from Prog_EcoEn.ecoen_app import views
from .views import CustomLoginView, CustomSignupView

urlpatterns = [
    # Página principal
    path('', views.index, name='index'),

    # Autenticación personalizada (renombradas para no chocar con Allauth)
    path("login/", CustomLoginView.as_view(), name="custom_login"),
    path("signup/", CustomSignupView.as_view(), name="custom_signup"),
    path("logout/", views.cerrar_sesion, name="custom_logout"),

    # Productos
    path("productos/", views.productos, name="productos"),
    path("producto/<int:id>/", views.producto_detalle, name="producto_detalle"),
    path("crear-producto/", views.crear_producto, name="crear_producto"),

    # Perfil
    path("perfil/", views.mi_perfil, name="mi_perfil"),
    path("perfil/editar/", views.editar_perfil, name="editar_perfil"),

    # Carrito y compras
    path("carrito/", views.carrito, name="carrito"),
    path("confirmar/<str:metodo>/", views.confirmar_pago, name="confirmar_pago"),

    # Opiniones
    path("opinion/", views.opinion_view, name="opinion"),

    # Allauth (solo para social login: Google, etc.)
    path("accounts/", include("allauth.urls")),
]
