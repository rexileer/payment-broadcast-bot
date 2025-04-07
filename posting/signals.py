from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PostingMessage
from bot.post_sender import send_posting

@receiver(post_save, sender=PostingMessage)
def send_posting_on_create(sender, instance, created, **kwargs):
    from django.utils.timezone import now
    print(f"[{now()}] Signal triggered for PostingMessage. Created: {created}")
    if created:
        try:
            send_posting(instance)
        except Exception as e:
            print(f"Ошибка в send_posting: {e}")
