from users.models import User
from asgiref.sync import sync_to_async
from django.utils.timezone import now
from datetime import timedelta


@sync_to_async
def get_all_users():
    return list(User.objects.all())

@sync_to_async
def unactivate_user(telegram_id):
    return User.objects.filter(telegram_id=telegram_id).update(is_active=False)

@sync_to_async
def activate_user(telegram_id):
    return User.objects.filter(telegram_id=telegram_id).update(is_active=True)

@sync_to_async
def banned_user(telegram_id):
    return User.objects.filter(telegram_id=telegram_id).update(not_banned=False)

@sync_to_async
def unbanned_user(telegram_id):
    return User.objects.filter(telegram_id=telegram_id).update(not_banned=True)

@sync_to_async
def get_user(telegram_id):
    try:
        return User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        return None

@sync_to_async
def update_user_payment(telegram_id):
    return User.objects.filter(telegram_id=telegram_id).update(subscription_until=now() + timedelta(days=180))