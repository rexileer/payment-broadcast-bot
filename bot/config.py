from django.conf import settings
from aiogram import Bot
from aiogram.client.bot import DefaultBotProperties

TOKEN = settings.TELEGRAM_BOT_TOKEN
bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode='HTML'))
