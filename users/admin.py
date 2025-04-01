from django.contrib import admin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('telegram_id', 'created_at', 'is_active', 'subscription_until', 'not_banned')
    list_filter = ('is_active', 'not_banned')