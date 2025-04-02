from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup


def send_payment_kb():
    inline_keyboard = []
    
    buttons = [
        InlineKeyboardButton(text="Оплатить", callback_data="payment"),
    ]
    inline_keyboard.append(buttons)

    return InlineKeyboardMarkup(inline_keyboard=inline_keyboard)