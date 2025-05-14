from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import PostingMessage
import requests
import os
from requests.exceptions import RequestException

@receiver(post_save, sender=PostingMessage)
def send_posting_on_create(sender, instance, created, **kwargs):
    from django.utils.timezone import now
    print(f"[{now()}] Signal triggered for PostingMessage. Created: {created}")
    if created:
        try:
            # Отправляем запрос к бот-сервису
            bot_service_url = os.getenv('BOT_SERVICE_URL', 'http://bot:8000')
            response = requests.post(
                f"{bot_service_url}/send_posting/",
                json={'posting_id': instance.id},
                timeout=5  # 5 секунд таймаут
            )
            if response.status_code != 200:
                print(f"Ошибка при отправке запроса к бот-сервису: {response.text}")
        except RequestException as e:
            print(f"Ошибка сети при отправке запроса к бот-сервису: {e}")
        except Exception as e:
            print(f"Неожиданная ошибка при отправке запроса к бот-сервису: {e}")
