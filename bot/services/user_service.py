from users.models import User
from asgiref.sync import sync_to_async


@sync_to_async
def get_all_users():
    return list(User.objects.all())