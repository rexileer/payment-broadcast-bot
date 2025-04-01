from django.db import models
from django.utils.timezone import now
from datetime import timedelta

class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def _default_subscription():
        return now() + timedelta(days=180)
    
    subscription_until = models.DateTimeField(default=_default_subscription(), blank=True)
        
    class Meta:
        verbose_name = 'Пользователь telegram'
        verbose_name_plural = 'Пользователи telegram'