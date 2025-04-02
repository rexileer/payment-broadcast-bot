from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


def send_payment_kb():
    reply_keyboard = []
    
    buttons = [
        KeyboardButton(text="/pay"),
    ]
    reply_keyboard.append(buttons)

    return ReplyKeyboardMarkup(
        keyboard=reply_keyboard,
        resize_keyboard=True,
        one_time_keyboard=True,
    )