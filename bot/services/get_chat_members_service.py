from pyrogram import Client, utils
from config import API_HASH, API_ID

import logging

logger = logging.getLogger(__name__)


def get_peer_type_new(peer_id: int) -> str:
    peer_id_str = str(peer_id)
    if not peer_id_str.startswith("-"):
        return "user"
    elif peer_id_str.startswith("-100"):
        return "channel"
    else:
        return "chat"

# Фикс: переопределяем стандартную функцию
utils.get_peer_type = get_peer_type_new


async def get_chat_members(chat_id):
    api_id = API_ID
    api_hash = API_HASH


    member_ids = []
    async with Client("s1", api_id, api_hash) as app:
        logger.info("Проверка доступа. chat: " + str(chat_id))
        chat = await app.get_chat(int(chat_id))  # Проверяет, "виден" ли чат
        await app.send_message(chat_id, "Проверка доступа")
        async for member in app.get_chat_members(chat_id):
            member_ids.append(member.user.id)
    return member_ids
