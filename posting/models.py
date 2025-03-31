from django.db import models
from django.utils.timezone import now


class PostingMessage(models.Model):
    text = models.TextField("Текст сообщения", blank=True, null=True)
    file = models.FileField("Медиафайл", upload_to="media/", blank=True, null=True)
    media_type = models.CharField(
        "Тип медиафайла",
        max_length=10,
        choices=[("image", "Изображение"), ("video", "Видео")],
        blank=True,
        null=True,
    )
    send_time = models.DateTimeField("Время отправки", default=now)

    def __str__(self):
        return f"Публикация {self.id}"
    
    class Meta:
        verbose_name = 'Публикация'
        verbose_name_plural = 'Публикации'