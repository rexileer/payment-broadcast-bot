from payment.models import PaymentMessage
from aiogram.exceptions import TelegramForbiddenError
from bot.config import bot_manager
from posting.models import FallbackNotificationMessage
import logging
from pyrogram.errors import PeerIdInvalid, UsernameInvalid, FloodWait
import asyncio

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
        # Используем userbot из текущего контейнера/сервиса
        logger.info(f"Инициализация userbot для fallback сообщения пользователю {user_id}")
        userbot = await bot_manager.get_userbot()
        
        try:
            # Пытаемся "познакомиться" с пользователем перед отправкой сообщения
            logger.info(f"Пытаемся получить информацию о пользователе {user_id}")
            try:
                # Пытаемся найти пользователя в общих чатах
                common_chats = await userbot.get_common_chats(user_id)
                logger.info(f"Найдено общих чатов с пользователем {user_id}: {len(common_chats)}")
            except PeerIdInvalid:
                # Если не нашли - пробуем получить диалоги и их участников
                logger.info(f"Не удалось найти общих чатов с {user_id}, пробуем получить диалоги")
                async for dialog in userbot.get_dialogs():
                    if dialog.chat.type in ["group", "supergroup"]:
                        try:
                            await userbot.get_chat_member(dialog.chat.id, user_id)
                            logger.info(f"Нашли пользователя {user_id} в чате {dialog.chat.title}")
                            break
                        except Exception:
                            continue
            
            # Пытаемся получить информацию о пользователе напрямую
            logger.info(f"Получаем информацию о пользователе {user_id}")
            user_info = await userbot.get_users(user_id)
            logger.info(f"Успешно получена информация о пользователе {user_id}: {user_info.first_name}")
        except Exception as e:
            logger.warning(f"Не удалось получить информацию о пользователе {user_id}: {e}")
            # Продолжаем попытку отправки сообщения даже если не удалось получить информацию
        
        # Пробуем отправить сообщение с повторными попытками
        max_retries = 3
        for attempt in range(1, max_retries + 1):
            try:
                logger.info(f"Отправляем fallback-сообщение через userbot пользователю {user_id} (попытка {attempt})")
                await userbot.send_message(chat_id=user_id, text=fallback_msg.text)
                logger.info(f"Fallback-сообщение отправлено через юзербота пользователю {user_id}")
                return True
            except FloodWait as e:
                logger.warning(f"FloodWait на {e.value} секунд при отправке сообщения {user_id}")
                if attempt < max_retries:
                    await asyncio.sleep(e.value + 1)
            except (PeerIdInvalid, UsernameInvalid):
                logger.error(f"Невозможно отправить сообщение пользователю {user_id}: пользователь не найден")
                return False
            except Exception as e:
                if attempt < max_retries:
                    logger.warning(f"Ошибка при отправке сообщения пользователю {user_id} (попытка {attempt}): {e}")
                    await asyncio.sleep(2)
                else:
                    raise
        
        return False
    except Exception as e:
        logger.error(f"Ошибка при отправке fallback-сообщения через юзербота пользователю {user_id}: {e}", exc_info=True)
        return False