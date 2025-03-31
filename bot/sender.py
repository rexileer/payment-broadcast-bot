from aiogram import Bot
import asyncio
from aiogram.types import FSInputFile

from django.conf import settings

TOKEN = settings.TELEGRAM_BOT_TOKEN


bot = Bot(token=TOKEN)

async def send_posting_to_group(posting):
    group_chat_id = -1002338995278
    text = posting.text or "Новая публикация!"
    media_type = posting.media_type
    file = posting.file
    
    # Если в объявлении есть медиафайл, можно проверить media_type и отправить фото или видео
    try:
        if file:
            if media_type == "image":
                image_input = FSInputFile(file.path)
                await bot.send_photo(chat_id=group_chat_id, photo=image_input, caption=text)
            elif media_type == "video":
                video_input = FSInputFile(file.path)
                await bot.send_video(chat_id=group_chat_id, video=video_input, caption=text)
        elif text:
            await bot.send_message(chat_id=group_chat_id, text=text)
    except Exception as e:
        print(f"Ошибка отправки публикации в группу: {e}, публикация: {posting}, токен: {TOKEN}")

def send_posting(posting):
    try:
        loop = asyncio.get_event_loop()
        if loop.is_closed():
            raise RuntimeError
    except RuntimeError:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
    loop.run_until_complete(send_posting_to_group(posting))
