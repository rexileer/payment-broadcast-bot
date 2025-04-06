from django.conf import settings
from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

# TELEGRAM
TOKEN = settings.TELEGRAM_BOT_TOKEN
GROUP_IDS = settings.TELEGRAM_GROUP_IDS

# PAYMENT
PROVIDER_TOKEN = settings.PROVIDER_TOKEN
TEST_PROVIDER_TOKEN = settings.TEST_PROVIDER_TOKEN
CURRENCY = settings.CURRENCY
PRICE = settings.PRICE

# API USERBOT
API_HASH = settings.API_HASH
API_ID = settings.API_ID

# SESSION BOT
session = AiohttpSession()
bot = Bot(token=TOKEN, session=session, default=DefaultBotProperties(parse_mode='HTML'))
