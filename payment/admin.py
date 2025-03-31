from django.contrib import admin
from .models import PaymentMessage

admin.site.site_header = "Редактирование"

@admin.register(PaymentMessage)
class StartCommandResponseAdmin(admin.ModelAdmin):
    def has_add_permission(self, request):
        return not PaymentMessage.objects.exists()  # Разрешаем добавлять, только если нет записей

    def has_delete_permission(self, request, obj=None):
        return False  # Запрещаем удаление

