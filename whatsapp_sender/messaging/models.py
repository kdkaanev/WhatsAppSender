from django.db import models

# Create your models here.
from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to="excel/")
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    
class Contact(models.Model):
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=20)

    def __str__(self):
        return self.name
    
    
class Message(models.Model):
    STATUS_CHOICES = (
        ("pending", "Pending"),
        ("sent", "Sent"),
        ("failed", "Failed"),
    )

    contact = models.ForeignKey(
        Contact,
        on_delete=models.CASCADE
    )

    text = models.TextField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="pending"
    )
    twilio_sid = models.CharField(
        max_length=100,
        blank=True
    )


    created_at = models.DateTimeField(auto_now_add=True)
    sent_at = models.DateTimeField(
        null=True,
        blank=True
    )