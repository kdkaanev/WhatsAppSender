import logging

from celery import shared_task
from django.utils import timezone

from .models import Message
from .services import WhatsAppService

logger = logging.getLogger(__name__)

class MessageStatus:
    PENDING = "pending"
    SENT = "sent"
    FAILED = "failed"
@shared_task(name="messaging.send_whatsapp_message")
def send_whatsapp_message(message_id: int) -> dict:
    try:
        message = (
            Message.objects
            #.select_for_update()
            .select_related("contact")
            .get(pk=message_id)
            )
    except Message.DoesNotExist:
        return {
            "success": False,
            "message_id": message_id,
            "error": "Message does not exist.",
        }
    if message.status == MessageStatus.SENT:
        return {
            "success": True,
            "message_id": message.id,
            "sid": message.twilio_sid,
            "status": message.status,
        }

    service = WhatsAppService()
    result = service.send_message(
        phone=message.contact.phone,
        text=message.text,
    )

    if result.get("success"):
        message.status = "sent"
        message.twilio_sid = result.get("sid", "")
        message.sent_at = timezone.now()
        #message.error_message = ""
        message.save(update_fields=["status", "twilio_sid", "sent_at",])
    else:
        message.status = "failed"
        #message.error_message = result.get("error", "")
        message.save(update_fields=["status", ])
    logger.info(
        f"Message {message.id} processing completed with status: {message.status}",
         extra={"message_id": message.id, "status": message.status}	
        )
    return {
        "message_id": message.id,
        **result,
    }
