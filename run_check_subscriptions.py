import os
import django
import asyncio
import logging

# Настройка Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.settings")
django.setup()

from bot.payment_sender import check_subscriptions  # Теперь можно импортировать Django-модели

# Настройка логирования
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

CHECK_INTERVAL_SECONDS = 5 * 60  # 5 минут

async def main():
    while True:
        try:
            logger.info("Запуск проверки подписок...")
            await check_subscriptions(logger=logger)
            logger.info("Проверка подписок завершена.")
        except Exception as e:
            logger.error(f"Ошибка в процессе проверки подписок: {e}")
        await asyncio.sleep(CHECK_INTERVAL_SECONDS)

if __name__ == "__main__":
    asyncio.run(main())