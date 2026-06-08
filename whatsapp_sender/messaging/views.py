from django.shortcuts import render

# Create your views here.
from .services import send_whatsapp_message

send_whatsapp_message(
    "+359898644178",
    "Тестово съобщение"
)