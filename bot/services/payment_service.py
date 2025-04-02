from payment.models import Payment
from bot.services.user_service import get_user, activate_user, update_user_payment

async def success_payment(telegram_id, amount, status, transaction_id):
    """Сохраняем платеж"""
    user = await get_user(telegram_id)
    if user:
        await activate_user(telegram_id)
        await update_user_payment(telegram_id)
    
    return await Payment.objects.acreate(
        user=user, 
        amount=amount, 
        status=status, 
        transaction_id=transaction_id
    )
