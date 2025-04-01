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

async def main():
    await check_subscriptions(logger=logger)

if __name__ == "__main__":
    asyncio.run(main())
