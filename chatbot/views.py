# chatbot/views.py
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def chatbot_home(request):
    return render(request, "chatbot/chat.html")

@csrf_exempt
def chatbot_response(request):
    if request.method == "POST":
        data = json.loads(request.body)
        user_message = data.get("message", "")
        reply = f"EcoBot recibió: {user_message}"
        return JsonResponse({"reply": reply})
    return JsonResponse({"reply": "Usa POST para comunicarte con EcoBot."})
