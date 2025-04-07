from datetime import timedelta
from django.utils.timezone import now
from payment.models import Payment
from users.models import UserChannelSubscription
from bot.services.user_service import get_user

from asgiref.sync import sync_to_async


async def success_payment(telegram_id, channel_id, amount, status, transaction_id):
    """Сохраняем платёж и продлеваем подписку пользователя на канал"""

    user = await get_user(telegram_id)
    if not user:
        return

    # Продлеваем или создаём подписку на канал
    try:
        subscription = await UserChannelSubscription.objects.aget(user=user, channel_id=channel_id)
        subscription.subscription_until = now() + timedelta(days=180)
        subscription.is_paid = True
        subscription.banned = False
        await sync_to_async(subscription.save)()
    except UserChannelSubscription.DoesNotExist:
        await UserChannelSubscription.objects.acreate(
            user=user,
            channel_id=channel_id,
            is_paid=True,
            banned=False,
            subscription_until=now() + timedelta(days=180)
        )

    # Сохраняем платёж
    return await Payment.objects.acreate(
        user=user,
        amount=amount,
        status=status,
        transaction_id=transaction_id
    )
