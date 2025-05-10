from payment.models import PaymentMessage
from aiogram.exceptions import TelegramForbiddenError
from bot.config import bot_manager
from posting.models import FallbackNotificationMessage
import logging

logger = logging.getLogger(__name__)


async def get_payment_message(channel) -> str:
    msg = await PaymentMessage.objects.afirst()
    return msg.text if msg else f"Ваша подписка на канал {channel.name} истекла. Пожалуйста, оплатите подписку для продолжения."


async def send_message_with_fallback(user_id: int, text: str):
    logger.warning(f"Основной бот не может отправить сообщение пользователю {user_id}, пробуем юзербота")
    # Получаем сообщение из базы
    fallback_msg = await FallbackNotificationMessage.objects.afirst()
    if not fallback_msg:
        logger.warning("Нет fallback-сообщения в базе")
        fallback_msg = FallbackNotificationMessage(text="Пожалуйста, оплатите подписку через бота для доступа к группе.")

    try:
        userbot = await bot_manager.get_userbot()
        await userbot.send_message(chat_id=user_id, text=fallback_msg.text)
        logger.info(f"Fallback-сообщение отправлено через юзербота {user_id}")
    except Exception as e:
        logger.error(f"Ошибка при отправке fallback-сообщения через юзербота {user_id}: {e}")