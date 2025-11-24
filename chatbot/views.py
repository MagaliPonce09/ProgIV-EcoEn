# chatbot/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def chatbot_home(request):
    # Renderiza el template chatbot.html que está en ecoen_app/templates/chatbot.html
    return render(request, "chatbot.html")

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({"reply": "Formato de datos inválido."})

        user_message = data.get("message", "")
        reply = f"EcoBot recibió: {user_message}"

        # Respuestas básicas de ejemplo
        if "energía" in user_message.lower():
            reply = "💡 Tip: Usa lámparas LED y desconecta cargadores."
        elif "asistencia" in user_message.lower():
            reply = "🔧 Contacta soporte en soporte@tuempresa.com."
        elif "compra" in user_message.lower():
            reply = "🛒 Puedes explorar productos en la sección 'Productos'."
        elif "tips" in user_message.lower():
            reply = "📘 Recuerda separar residuos y ahorrar agua."

        return JsonResponse({"reply": reply})

    return JsonResponse({"reply": "Usa POST para comunicarte con EcoBot."})
