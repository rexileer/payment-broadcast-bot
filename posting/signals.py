from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PostingMessage
from bot.post_sender import send_posting

@receiver(post_save, sender=PostingMessage)
def send_posting_on_create(sender, instance, created, **kwargs):
    if created:
        send_posting(instance)
        pass