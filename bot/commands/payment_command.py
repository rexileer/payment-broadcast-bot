from aiogram import Router, F
from aiogram.types import Message, LabeledPrice, PreCheckoutQuery
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from config import bot
from payment_config import config
from bot.services.payment_service import success_payment

import logging
logger = logging.getLogger(__name__)

router = Router()


class FSMPrompt(StatesGroup):
    buying = State()
    

@router.message(Command(commands=['pay']))
async def buy_subscription(message: Message, state: FSMContext):
    try:
            # Проверка состояния и его очистка
            current_state = await state.get_state()
            if current_state is not None:
                await state.clear()  # чтобы свободно перейти сюда из любого другого состояния
            
            if config.provider_token.split(':')[1] == 'TEST':
                await message.reply("Для оплаты используйте данные тестовой карты: 1111 1111 1111 1026, 12/22, CVC 000.")

            prices = [LabeledPrice(label='Оплата заказа', amount=config.price)]
            await state.set_state(FSMPrompt.buying)
            await bot.send_invoice(
                chat_id=message.chat.id,
                title='Покупка',
                description='Оплата подписки на 6 месяцев',
                payload='bot_paid',
                provider_token=config.provider_token,
                currency="RUB",
                prices=prices,
                # need_phone_number=True,
                # send_phone_number_to_provider=True,
                # provider_data=config.provider_data
            )
    except Exception as e:
        logging.error(
            f"Ошибка при выполнении команды /pay: {e}\n"
            f"Данные: {message.chat.id}\n{message.from_user.id}\n"
            f"{message.from_user.username}\n{config.provider_token}\n{config.currency}\n{config.price}\n{config.provider_data}"
            )
        await message.answer("Произошла ошибка при обработке команды!")
        current_state = await state.get_state()
        if current_state is not None:
            await state.clear()
            
@router.pre_checkout_query()
async def process_pre_checkout_query(pre_checkout_query: PreCheckoutQuery):
    try:
        await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)  # всегда отвечаем утвердительно
    except Exception as e:
        logging.error(f"Ошибка при обработке апдейта типа PreCheckoutQuery: {e}")
        

@router.message(F.successful_payment)
async def process_successful_payment(message: Message, state: FSMContext):
    try:
        amount = message.successful_payment.total_amount
        status = message.successful_payment.invoice_payload
        transaction_id = message.successful_payment.provider_payment_charge_id
        await message.reply(f"Платеж на сумму {amount // 100} "
                            f"{message.successful_payment.currency} прошел успешно!")
        await success_payment(message.from_user.id, amount, status, transaction_id)
        logging.info(f"Получен платеж от {message.from_user.id}")
    except Exception as e:
        logging.error(f"Ошибка при обработке сообщения об успешном платеже: {e}")
        await message.reply("Произошла ошибка при обработке платежа!")
    current_state = await state.get_state()
    if current_state is not None:
        await state.clear()  # чтобы свободно перейти сюда из любого другого состояния

            
@router.message(FSMPrompt.buying)
async def process_unsuccessful_payment(message: Message, state: FSMContext):
        await message.reply("Не удалось выполнить платеж!")
        current_state = await state.get_state()
        if current_state is not None:
            await state.clear()  # чтобы свободно перейти сюда из любого другого состояния