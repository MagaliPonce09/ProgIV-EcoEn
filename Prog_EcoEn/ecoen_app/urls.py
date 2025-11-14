from django.urls import path, include
<<<<<<< HEAD
from .views import chatbot_view



@csrf_exempt
def chatbot_view(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")

        # Llamada al modelo de IA
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",  # o el modelo que uses
            messages=[{"role": "user", "content": user_message}]
        )

        bot_reply = response["choices"][0]["message"]["content"]
        return JsonResponse({"reply": bot_reply})

=======
from Prog_EcoEn.ecoen_app import views
from .views import CustomLoginView, CustomSignupView
>>>>>>> 1e1cde8f33ebc315da7b2eae982ebf2c723b4289

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
<<<<<<< HEAD
    path("chat/", chatbot_view, name="chatbot"),
=======

    # Carrito y compras
    path("carrito/", views.carrito, name="carrito"),
    path("confirmar/<str:metodo>/", views.confirmar_pago, name="confirmar_pago"),

    # Opiniones
    path("opinion/", views.opinion_view, name="opinion"),

    # Allauth (solo para social login: Google, etc.)
    path("accounts/", include("allauth.urls")),
>>>>>>> 1e1cde8f33ebc315da7b2eae982ebf2c723b4289
]
