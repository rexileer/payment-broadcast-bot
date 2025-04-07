from pyrogram import Client, utils
from config import API_HASH, API_ID
from users.models import User, Channel, UserChannelSubscription
from django.utils.timezone import now
from datetime import timedelta
import logging

logger = logging.getLogger(__name__)

def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"

# Переопределяем Pyrogram функцию
utils.get_peer_type = get_peer_type_new

async def get_chat_members(chat_id):
    api_id = API_ID
    api_hash = API_HASH
    added_users = 0
    updated_subs = 0

    async with Client("s1", api_id, api_hash) as app:
        logger.info(f"Проверка доступа к чату: {chat_id}")
        chat = await app.get_chat(int(chat_id))

        # Добавляем канал в БД, если ещё не добавлен
        channel, _ = await Channel.objects.aupdate_or_create(
            channel_id=chat.id,
            defaults={
                "name": chat.title or f"Channel {chat.id}",
                "link": f"https://t.me/{chat.username}" if chat.username else "",
                "is_active": True
            }
        )

        # await app.send_message(chat_id, "Проверка доступа")

        async for member in app.get_chat_members(chat_id):
            user_id = member.user.id
            user, _ = await User.objects.aupdate_or_create(telegram_id=user_id)

            # Добавляем или обновляем подписку
            subscription_defaults = {
                "subscription_until": now() + timedelta(days=180),
                "is_paid": True,
                "banned": False
            }
            obj, created = await UserChannelSubscription.objects.aupdate_or_create(
                user=user,
                channel=channel,
                defaults=subscription_defaults
            )
            if created:
                added_users += 1
            else:
                updated_subs += 1

    logger.info(f"Добавлено пользователей: {added_users}, обновлено подписок: {updated_subs}")
    return added_users, updated_subs
