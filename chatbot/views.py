from django.shortcuts import render
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.utils.html import escape


def chat_page(request):
    return render(request, 'chatbot/chat.html')


@require_POST

def chatbot_response(request):
    user_message = request.POST.get('message', '').strip()
    # Sanear mensaje por seguridad básica
    user_message_safe = escape(user_message)

    # Lógica simple del bot (placeholder)
    if not user_message_safe:
        reply = "Escribime algo y te respondo."
    elif "hola" in user_message_safe.lower():
        reply = "¡Hola! ¿Cómo te puedo ayudar hoy?"
    elif "precio" in user_message_safe.lower():
        reply = "Los precios varían según el producto y la potencia. ¿Qué producto te interesa?"
    elif "panel" in user_message_safe.lower():
        reply = "Los paneles solares monocristalinos son más eficientes. ¿Buscás información de instalación o rendimiento?"
    else:
        reply = "No entendí bien. Podés preguntarme sobre productos, precios, instalación o soporte."

    return JsonResponse({
        "response": reply
    })