import pandas as pd

from .models import Contact, Message
from .tasks import send_whatsapp_message

def import_excel(file_path):

    df = pd.read_excel(file_path)

    for _, row in df.iterrows():

        contact, _ = Contact.objects.get_or_create(
            phone=str(row["phone"]),
            defaults={
                "name": row["name"]
            }
        )

        message = Message.objects.create(
            contact=contact,
            text=row["message"],
        )
        send_whatsapp_message.delay(message.id)