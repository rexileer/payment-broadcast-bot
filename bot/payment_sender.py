from django.utils.timezone import now, timedelta
from bot.config import bot
from bot.services.payment_message_service import get_payment_message
from bot.services.channels_service import get_all_channels, get_channel_subscriptions
from bot.keyboards.reply.to_payment_kb import send_payment_kb
from asgiref.sync import sync_to_async

import logging
logger = logging.getLogger(__name__)


async def check_subscriptions(logger=logger):
    """Проверяет подписки на все каналы, уведомляет и банит при просрочке"""

    channels = await get_all_channels()

    for channel in channels:
        group_id = str(channel.channel_id)

        # Все подписки на канал (сервис, sync_to_async)
        subscriptions = await sync_to_async(get_channel_subscriptions)(channel)

        for subscription in subscriptions:
            if subscription.subscription_until <= now():

                user = subscription.user
                telegram_id = user.telegram_id

                if subscription.banned:
                    continue  # уже обработан

                time_diff = now() - subscription.subscription_until

                # Если прошло более 1 суток с окончания подписки — баним
                if time_diff > timedelta(days=1):
                    try:
                        await bot.ban_chat_member(group_id, telegram_id)
                        # await bot.unban_chat_member(group_id, telegram_id)
                        subscription.banned = True
                        subscription.is_paid = False
                        await sync_to_async(subscription.save)()
                        logger.info(f"Забанили пользователя {telegram_id} за неуплату в канале {channel.name}")
                    except Exception as e:
                        logger.error(f"Ошибка при бане {telegram_id} в канале {channel.name}: {e}")

                elif subscription.is_paid:
                    # Отправляем напоминание, если ещё не забанен
                    try:
                        message = await get_payment_message()
                        keyboard = send_payment_kb()
                        await bot.send_message(
                            telegram_id,
                            f"{message}\n\nДля канала: {channel.name}",
                            reply_markup=keyboard
                        )
                        subscription.is_paid = False
                        await sync_to_async(subscription.save)()
                        logger.info(f"Оповестили пользователя {telegram_id} о платеже за канал {channel.name}")
                    except Exception as e:
                        logger.error(f"Ошибка при уведомлении {telegram_id} за канал {channel.name}: {e}. Вероятно, пользователь не подписан на бота")
                        # Баним, так как не смогли отправить уведомление
                        try:
                            await bot.ban_chat_member(group_id, telegram_id)
                            # await bot.unban_chat_member(group_id, telegram_id)
                            subscription.banned = True
                            subscription.is_paid = False
                            await sync_to_async(subscription.save)()
                            logger.info(f"Забанили пользователя {telegram_id} за неуплату в канале {channel.name}")
                        except Exception as e:
                            logger.error(f"Ошибка при бане {telegram_id} в канале {channel.name}: {e}")
