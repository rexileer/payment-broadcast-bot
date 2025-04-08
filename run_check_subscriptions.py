import os
import django
import asyncio
import logging

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from bot.payment_sender import check_subscriptions
from bot.services.chat_member_updater import update_all_channels_users  # создадим ниже

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

CHECK_INTERVAL_SECONDS = 5 * 60  # каждые 5 минут

async def main():
    while True:
        try:
            logger.info("▶️ Запуск проверки подписок...")
            await check_subscriptions(logger=logger)
            logger.info("✅ Подписки проверены.")

            logger.info("▶️ Сканирование каналов...")
            await update_all_channels_users()
            logger.info("✅ Каналы просканированы.")
        except Exception as e:
            logger.error(f"💥 Ошибка в фоновом процессе: {e}")
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())
