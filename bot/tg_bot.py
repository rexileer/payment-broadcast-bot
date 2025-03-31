import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
os.environ.update({'DJANGO_ALLOW_ASYNC_UNSAFE': "true"})

import django
django.setup()

import asyncio
from aiogram import Bot, Dispatcher
from aiogram.client.bot import DefaultBotProperties

from django.conf import settings

import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('bot_logs.log', mode='a')  # Запись логов в файл 'bot_logs.log'
    ]
)

logger = logging.getLogger(__name__)

TOKEN = settings.TELEGRAM_BOT_TOKEN

async def main():
    try:
        bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
        dp = Dispatcher()
        
        
        await asyncio.gather(
            bot.delete_webhook(drop_pending_updates=True),
            dp.start_polling(bot),
        )
    finally:
        await bot.close()

if __name__ == "__main__":
    asyncio.run(main())