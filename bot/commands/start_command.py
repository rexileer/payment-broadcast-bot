from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from services.start_service import get_start_message

import logging
logger = logging.getLogger(__name__)

router = Router()

@router.message(CommandStart())
async def start(message: Message):
    logger.info(f"Received /start command from {message.from_user.id}")
    try:
        text = await get_start_message()
    except Exception as e:
        logger.error(f"Error getting start message: {e}")
        text = "Добро пожаловать в бота"
    await message.delete()
    await message.answer(text, reply_markup=None)