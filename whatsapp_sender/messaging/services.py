# messaging/services.py

from twilio.rest import Client
from django.conf import settings


client = Client(
    settings.TWILIO_ACCOUNT_SID,
    settings.TWILIO_AUTH_TOKEN
)
    
class WhatsAppService:

    def __init__(self):
        self.client = Client(
            settings.TWILIO_ACCOUNT_SID,
            settings.TWILIO_AUTH_TOKEN
        )

    def send_message(self, phone, text):
        try:
            message = self.client.messages.create(
                body=text,
                from_=settings.TWILIO_WHATSAPP_FROM,
                to=f"whatsapp:{phone}"
            )

            return {
                "success": True,
                "sid": message.sid,
                "status": message.status,
            }

        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
        