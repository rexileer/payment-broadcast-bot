from payment.models import PaymentMessage


async def get_payment_message():
    msg = await PaymentMessage.objects.afirst()
    return msg.text if msg else "Пожалуйста, оплатите подписку для доступа к группе.\n Для этого введите команду /pay"