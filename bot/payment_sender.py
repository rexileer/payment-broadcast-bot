from django.utils.timezone import now
from bot.config import bot, GROUP_ID
from bot.services.payment_message_service import get_payment_message
from bot.services.user_service import get_all_users, unactivate_user
from bot.keyboards.reply.to_payment_kb import send_payment_kb

import logging
logger = logging.getLogger(__name__)

async def check_subscriptions(logger=logger):
    """Проверяет подписки, отправляет ссылку на оплату, кикает неактивных"""
    
    # 1. Кикаем пользователей, у которых подписка истекла и они уже неактивны
    users = await get_all_users()
    
    expired_and_inactive_users = [user for user in users if user.subscription_until <= now() and not user.is_active]
    logger.info(f"Пользователи, которых надо кикнуть: {[user.telegram_id for user in expired_and_inactive_users]}")
    logger.info(f"Кикаем {len(expired_and_inactive_users)} пользователей из чата {GROUP_ID}")

    for user in expired_and_inactive_users:
        try:
            await bot.ban_chat_member(str(GROUP_ID), user.telegram_id)
            await bot.unban_chat_member(str(GROUP_ID), user.telegram_id)  # Разбан, чтобы мог вернуться
            logger.info(f"Забанили пользователя {user.telegram_id} за неуплату")
        except Exception as e:
            logger.error(f"Ошибка при кике {user.telegram_id}: {e}")

    # 2. Отправляем сообщение пользователям, у которых подписка истекла, но они ещё активны
    expired_and_active_users = [user for user in users if user.subscription_until <= now() and user.is_active]
    logger.info(f"Пользователи, получающие оповещение: {[user.telegram_id for user in expired_and_active_users]}")
    logger.info(f"Отправляем оповещение {len(expired_and_active_users)} пользователям")

    for user in expired_and_active_users:
        logger.info(f"Пользователю {user.telegram_id} отправляем оповещение")
        try:
            message = await get_payment_message()
            keyboard = send_payment_kb()
            await bot.send_message(user.telegram_id, f"{message}", reply_markup=keyboard)

            # Делаем пользователя неактивным
            await unactivate_user(user.telegram_id)
            logger.info(f"Отправили оповещение пользователю {user.telegram_id}, деактивировали его")

        except Exception as e:
            logger.error(f"Ошибка при отправке уведомления пользователю {user.telegram_id}: {e}")
