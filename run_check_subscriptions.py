import os
import django
import asyncio
import logging
from datetime import datetime, timedelta

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from bot.payment_sender import check_subscriptions
from bot.services.chat_member_updater import update_all_channels_users
from bot.config import bot_manager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

CHECK_INTERVAL_SECONDS = 15 * 60  # каждые 15 минут
last_check_time = None

async def init_bots():
    """Инициализация ботов при старте"""
    try:
        # Ждем 5 секунд перед инициализацией
        await asyncio.sleep(10)
        # Инициализируем юзербота заранее с отдельной сессией
        await bot_manager.get_userbot(session_type='checker')
        logger.info("✅ Боты успешно инициализированы")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации ботов: {e}")
        raise

async def main():
    global last_check_time
    
    try:
        # Инициализируем ботов перед стартом
        await init_bots()
        
        while True:
            try:
                current_time = datetime.now()
                
                # Проверяем, прошло ли достаточно времени с последней проверки
                if last_check_time and (current_time - last_check_time).total_seconds() < CHECK_INTERVAL_SECONDS:
                    await asyncio.sleep(60)  # Спим минуту перед следующей проверкой
                    continue
                    
                logger.info("▶️ Запуск проверки подписок...")
                await check_subscriptions(logger=logger)
                logger.info("✅ Подписки проверены.")

                logger.info("▶️ Сканирование каналов...")
                await update_all_channels_users()
                logger.info("✅ Каналы просканированы.")
                
                last_check_time = current_time
                
            except Exception as e:
                logger.error(f"💥 Ошибка в фоновом процессе: {e}")
                await asyncio.sleep(60)  # При ошибке ждем минуту перед повторной попыткой
            else:
                await asyncio.sleep(60)  # Спим минуту перед следующей проверкой
    finally:
        # Закрываем соединения при выходе
        await bot_manager.close()

if __name__ == "__main__":
    asyncio.run(main())
