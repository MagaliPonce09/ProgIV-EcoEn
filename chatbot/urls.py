from django.urls import path
from .views import chat_page, chatbot_response

urlpatterns = [
    path('', chat_page, name='chat_page'),  # interfaz del chat
    path('respond/', chatbot_response, name='chatbot_response'),  # endpoint AJAX
]
