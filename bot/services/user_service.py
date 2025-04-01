from users.models import User
from asgiref.sync import sync_to_async


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
def get_user(telegram_id):
    try:
        return User.objects.get(telegram_id=telegram_id)
    except User.DoesNotExist:
        return None