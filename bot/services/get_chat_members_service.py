from pyrogram import utils
from bot.config import bot_manager
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
    added_users = 0
    updated_subs = 0

    try:
        app = await bot_manager.get_userbot()
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

        async for member in app.get_chat_members(chat_id):
            user_id = member.user.id
            user_name = member.user.username or f"{member.user.first_name} {member.user.last_name or ''}".strip()
            
            # Используем get_or_create вместо update_or_create
            user, created = await User.objects.aget_or_create(
                telegram_id=user_id,
                defaults={"name": user_name}
            )

            # Проверяем, есть ли уже подписка
            exists = await UserChannelSubscription.objects.filter(user=user, channel=channel).aexists()
            
            if not exists:
                await UserChannelSubscription.objects.acreate(
                    user=user,
                    channel=channel,
                    subscription_until=now() + timedelta(days=180),
                    is_paid=True,
                    banned=False
                )
                added_users += 1

        logger.info(f"Добавлено пользователей: {added_users}, обновлено подписок: {updated_subs}")
        return added_users, updated_subs
    except Exception as e:
        logger.error(f"Ошибка при получении участников чата {chat_id}: {e}")
        raise
