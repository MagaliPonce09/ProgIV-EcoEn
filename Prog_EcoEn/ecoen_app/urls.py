from django.urls import path
from . import views
from django.urls import path, include
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


urlpatterns = [
    path('', views.index, name='index'),
    path("registro/", views.registro, name="registro"),
    path("login/", views.iniciar_sesion, name="login"),
    path("logout/", views.cerrar_sesion, name="logout"),
    path("productos/", views.productos, name="productos"),
    path('accounts/', include('allauth.urls')),
    path("producto/<int:id>/", views.producto_detalle, name="producto_detalle"),
    path("perfil/", views.mi_perfil, name="mi_perfil"),
    path("perfil/editar/", views.editar_perfil, name="editar_perfil"),
    path("chat/", chatbot_view, name="chatbot"),
]
