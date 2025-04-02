from django.conf import settings
from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties
from aiogram.client.session.aiohttp import AiohttpSession

TOKEN = settings.TELEGRAM_BOT_TOKEN
GROUP_ID = settings.TELEGRAM_GROUP_ID
PROVIDER_TOKEN = settings.PROVIDER_TOKEN
TEST_PROVIDER_TOKEN = settings.TEST_PROVIDER_TOKEN
CURRENCY = settings.CURRENCY
PRICE = settings.PRICE
session = AiohttpSession()
bot = Bot(token=TOKEN, session=session, default=DefaultBotProperties(parse_mode='HTML'))
