from aiogram import Router, F
from aiogram.types import CallbackQuery


import logging
logger = logging.getLogger(__name__)

router = Router()


@router.callback_query(F.data == "payment")
async def start_filtering_callback(callback: CallbackQuery):
    user_id = callback.from_user.id


    await callback.message.edit_text("проводим оплату")