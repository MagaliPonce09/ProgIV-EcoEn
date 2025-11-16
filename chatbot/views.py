from django.shortcuts import render


def chatbot_home(request):
    return render(request, 'chatbot/chat.html')