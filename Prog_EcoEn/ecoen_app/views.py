from django.contrib.auth import login, logout
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from openai import AzureOpenAI
from django.conf import settings
from .models import Producto, Opinion, Compra, Puntuacion, Perfil
from .forms import EditarPerfilForm
from allauth.account.views import LoginView, SignupView
from django.utils import timezone

# =========================
# CHATBOT VIEW (flujo educativo + compra + opciones dinámicas)
# =========================
@csrf_exempt
def chatbot_response(request):
    if request.method != "POST":
        return JsonResponse({"reply": "Usa POST para comunicarte con EcoBot."})

    try:
        data = json.loads(request.body.decode("utf-8"))
    except Exception:
        return JsonResponse({"reply": "No pude leer tu mensaje. Intenta de nuevo."})

    user_message = data.get("message", "").lower().strip()
    options = []

    if "asistencia técnica" in user_message:
        reply = "🔧 Claro, cuéntame el problema. ¿Es con un panel solar, una lámpara LED, o el proceso de compra?"
        options = [
            {"label": "Panel solar", "send": "Asistencia: Panel solar"},
            {"label": "Lámpara LED", "send": "Asistencia: Lámpara LED"},
            {"label": "Proceso de compra", "send": "Asistencia: Compra"},
        ]

    elif "recomendación de productos" in user_message:
        reply = "🌱 ¿Qué categoría te interesa?"
        options = [
            {"label": "Energía solar ☀️", "send": "Categoría: Energía solar"},
            {"label": "Iluminación LED 💡", "send": "Categoría: Iluminación LED"},
            {"label": "Packaging reciclable 📦", "send": "Categoría: Packaging reciclable"},
        ]

    elif "realizar compra" in user_message or user_message.startswith("categoría:"):
        if "energía solar" in user_message:
            reply = "☀️ Elige un producto:"
            options = [
                {"label": "Kit solar básico 🔋", "send": "Producto: Kit solar básico"},
                {"label": "Panel solar portátil ☀️", "send": "Producto: Panel solar portátil"},
            ]
        elif "iluminación led" in user_message:
            reply = "💡 Elige un producto:"
            options = [
                {"label": "Lámpara LED eco", "send": "Producto: Lámpara LED eco"},
                {"label": "Tira LED eficiente", "send": "Producto: Tira LED eficiente"},
            ]
        elif "packaging reciclable" in user_message:
            reply = "📦 Elige un producto:"
            options = [
                {"label": "Bolsas reciclables", "send": "Producto: Bolsas reciclables"},
                {"label": "Cajas kraft eco", "send": "Producto: Cajas kraft eco"},
            ]
        else:
            reply = "🛒 Elige una categoría para comprar:"
            options = [
                {"label": "Energía solar ☀️", "send": "Categoría: Energía solar"},
                {"label": "Iluminación LED 💡", "send": "Categoría: Iluminación LED"},
                {"label": "Packaging reciclable 📦", "send": "Categoría: Packaging reciclable"},
            ]

    elif user_message.startswith("producto:"):
        producto = user_message.replace("producto:", "").strip()
        reply = f"¿Confirmás la compra de {producto.title()}?"
        options = [
            {"label": "✅ Confirmar compra", "send": f"Confirmar compra: {producto}"},
            {"label": "❌ Cancelar", "send": "Cancelar compra"},
        ]

    elif "confirmar compra" in user_message:
        reply = "✅ Añadido al carrito. Ve al carrito para finalizar: /carrito"
        options = [
            {"label": "Ir al carrito 🛒", "send": "Ir al carrito"},
            {"label": "Seguir explorando 🌿", "send": "Recomendación de productos"},
        ]

    elif "cancelar compra" in user_message:
        reply = "❌ Compra cancelada. ¿Te muestro otras categorías?"
        options = [
            {"label": "Ver categorías", "send": "Recomendación de productos"},
            {"label": "Tips de sostenibilidad", "send": "Tips de sostenibilidad"},
        ]

    elif "tips de sostenibilidad" in user_message or user_message.startswith("tip:"):
        if "ahorro de energía" in user_message:
            reply = ("⚡ Apaga dispositivos en standby y usa lámparas LED para reducir consumo. "
                     "👉 Sugerido: Lámparas LED eco.")
            options = [
                {"label": "Ver lámparas LED 💡", "send": "Categoría: Iluminación LED"},
                {"label": "Más tips", "send": "Más tips energía"},
            ]
        elif "reciclaje" in user_message:
            reply = ("♻️ Separa residuos orgánicos e inorgánicos; vidrio y aluminio se reciclan infinitamente. "
                     "👉 Sugerido: Bolsas reciclables y kits de separación.")
            options = [
                {"label": "Ver bolsas reciclables 📦", "send": "Categoría: Packaging reciclable"},
                {"label": "Más tips", "send": "Más tips reciclaje"},
            ]
        elif "movilidad verde" in user_message:
            reply = ("🚲 Usa bici o transporte público para reducir emisiones. "
                     "👉 Sugerido: Mochilas eco resistentes al agua.")
            options = [
                {"label": "Explorar accesorios 🌿", "send": "Recomendación de productos"},
                {"label": "Más tips", "send": "Más tips movilidad"},
            ]
        else:
            reply = "📘 Elige un tema de tips:"
            options = [
                {"label": "⚡ Ahorro de energía", "send": "Tip: Ahorro de energía"},
                {"label": "♻️ Reciclaje", "send": "Tip: Reciclaje"},
                {"label": "🚲 Movilidad verde", "send": "Tip: Movilidad verde"},
            ]

    else:
        reply = ("Soy EcoBot 🌍. Puedo ayudar con asistencia técnica, recomendación de productos, "
                 "realizar compra y tips de sostenibilidad.")
        options = [
            {"label": "🔧 Asistencia técnica", "send": "Asistencia técnica"},
            {"label": "🌱 Recomendación de productos", "send": "Recomendación de productos"},
            {"label": "🛒 Realizar compra", "send": "Realizar compra"},
            {"label": "📘 Tips de sostenibilidad", "send": "Tips de sostenibilidad"},
        ]

    return JsonResponse({"reply": reply, "options": options})

# =========================
# Vistas existentes
# =========================
def index(request):
    productos = Producto.objects.all()
    puntuaciones_usuario = {}

    if request.user.is_authenticated:
        puntuaciones = Puntuacion.objects.filter(usuario=request.user)
        puntuaciones_usuario = {p.producto_id: p.valor for p in puntuaciones}

    for producto in productos:
        producto.puntuacion_usuario = puntuaciones_usuario.get(producto.id, 0)

    opiniones = Opinion.objects.all()

    context = {
        "productos": productos,
        "opiniones": opiniones,
    }
    return render(request, "index.html", context)

class CustomLoginView(LoginView):
    template_name = "account/login.html"

class CustomSignupView(SignupView):
    template_name = "account/signup.html"

# ... (el resto de tus vistas se mantiene igual)
