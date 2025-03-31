from django.db import models


class User(models.Model):
    telegram_id = models.BigIntegerField(unique=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    subscription_until = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        verbose_name = 'Пользователь telegram'
        verbose_name_plural = 'Пользователи telegram'