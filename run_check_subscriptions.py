import os
import django
import asyncio
import logging
from datetime import datetime, timedelta

# Устанавливаем тип сервиса для правильного выбора сессии в config.py
os.environ["SERVICE_TYPE"] = "checker"

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from bot.payment_sender import check_subscriptions
from bot.services.chat_member_updater import update_all_channels_users
from bot.config import bot_manager

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(module)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('subscription_checker.log', mode='a')
    ]
)
logger = logging.getLogger(__name__)

CHECK_INTERVAL_SECONDS = 15 * 60  # каждые 15 минут
last_check_time = None

async def init_bots():
    """Инициализация ботов при старте"""
    try:
        logger.info("Инициализация Pyrogram Client для проверки подписок...")
        # Ждем 5 секунд перед инициализацией
        await asyncio.sleep(10)
        # Инициализируем юзербота с отдельной сессией для чекера
        await bot_manager.get_userbot()
        logger.info("✅ Userbot для проверки подписок успешно инициализирован")
    except Exception as e:
        logger.error(f"❌ Ошибка инициализации userbot: {e}")
        raise

async def main():
    global last_check_time
    
    logger.info("🚀 Запуск сервиса проверки подписок")
    
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
                logger.info(f"⏰ Следующая проверка через {CHECK_INTERVAL_SECONDS/60} минут")
                
            except Exception as e:
                logger.error(f"💥 Ошибка в фоновом процессе: {e}", exc_info=True)
                await asyncio.sleep(60)  # При ошибке ждем минуту перед повторной попыткой
            else:
                await asyncio.sleep(60)  # Спим минуту перед следующей проверкой
    finally:
        # Закрываем соединения при выходе
        logger.info("Завершение работы сервиса проверки подписок")
        await bot_manager.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        logger.info("Сервис проверки подписок остановлен")
    except Exception as e:
        logger.critical(f"Критическая ошибка в сервисе проверки подписок: {e}", exc_info=True)
