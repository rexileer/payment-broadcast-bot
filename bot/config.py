from django.conf import settings
from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession
from pyrogram import Client
import logging
import os

logger = logging.getLogger(__name__)

# TELEGRAM
TOKEN = settings.TELEGRAM_BOT_TOKEN

# PAYMENT
PROVIDER_TOKEN = settings.PROVIDER_TOKEN
TEST_PROVIDER_TOKEN = settings.TEST_PROVIDER_TOKEN
CURRENCY = settings.CURRENCY
PRICE = settings.PRICE

# API USERBOT
API_HASH = settings.API_HASH
API_ID = settings.API_ID

class BotManager:
    _instance = None
    _bot = None
    _userbot = None
    _session = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(BotManager, cls).__new__(cls)
            cls._session = AiohttpSession()
            cls._bot = Bot(token=TOKEN, session=cls._session, default=DefaultBotProperties(parse_mode='HTML'))
        return cls._instance

    @property
    def bot(self):
        return self._bot

    async def get_userbot(self):
        if self._userbot is None:
            try:
                # Используем абсолютный путь для сессии
                session_path = os.path.join(os.getcwd(), "bot", "s1_bot")
                self._userbot = Client(session_path, API_ID, API_HASH)
                await self._userbot.start()
                logger.info("✅ Userbot успешно инициализирован")
            except Exception as e:
                logger.error(f"❌ Ошибка инициализации юзербота: {e}")
                raise
        return self._userbot

    async def close(self):
        if self._bot:
            await self._bot.close()
        if self._userbot:
            await self._userbot.stop()

# Create singleton instance
bot_manager = BotManager()
bot = bot_manager.bot
