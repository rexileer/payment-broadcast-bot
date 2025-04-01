import asyncio
import threading
import logging
from bot.config import bot
from aiogram.types import FSInputFile
from bot.services.user_service import get_all_users
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter

logger = logging.getLogger('Posting')

loop = asyncio.new_event_loop()

def start_loop(loop):
    asyncio.set_event_loop(loop)
    loop.run_forever()

threading.Thread(target=start_loop, args=(loop,), daemon=True).start()


async def send_posting_to_users(posting):
    text = posting.text or "Новая публикация!"
    media_type = posting.media_type
    file = posting.file
    users = await get_all_users()

    for user in users:
        await asyncio.sleep(0.05)  # Минимальная задержка
        await send_message(user.telegram_id, text, file, media_type)

async def send_message(user_id, text=None, file=None, media_type=None):
    try:
        if file:
            if media_type == "image":
                image_input = FSInputFile(file.path)
                await bot.send_photo(user_id, image_input, caption=text)
            elif media_type == "video":
                video_input = FSInputFile(file.path)
                await bot.send_video(user_id, video_input, caption=text)
            else:
                logger.warning(f"Неизвестный тип медиафайла {media_type}")
        elif text:
            await bot.send_message(user_id, text)
        else:
            logger.warning("Пустая рассылка")
        
        logger.info(f"Сообщение отправлено {user_id}")

    except TelegramForbiddenError:
        logger.info(f"Пользователь {user_id} заблокировал бота. Сообщение не отправлено.")

    except TelegramRetryAfter as e:
        logger.error(f"⏳ Превышен лимит запросов к Telegram API: ожидание {e.retry_after} сек.")
        await asyncio.sleep(e.retry_after)
        await send_message(user_id, text, file, media_type)

    except Exception as e:
        logger.error(f"Ошибка отправки {user_id}: {e}")

def send_posting(posting):
    try:
        asyncio.run_coroutine_threadsafe(send_posting_to_users(posting), loop)
    except Exception as e:
        logger.error(f"Ошибка запуска рассылки: {e}")
