from aiogram import Router
from aiogram.types import Message
from aiogram.filters import Command
from services.get_chat_members_service import get_chat_members
from config import GROUP_IDS

import logging
logger = logging.getLogger(__name__)

router = Router()

@router.message(Command('all_members'))
async def cmd_all_members(message: Message):
    chat_ids = GROUP_IDS.split(',')
    for chat_id in chat_ids:
        await message.reply(f"Chat ID: {chat_id}")
        members_id = await get_chat_members(chat_id)
        await message.reply(f"Found members_id with IDs: {', '.join(str(id) for id in members_id)} in the chat.")