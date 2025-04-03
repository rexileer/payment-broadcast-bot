# payment-broadcast-bot
 
# cron commands
- sed -i 's/\r//g' /etc/cron.d/mycron
- crontab /etc/cron.d/mycron
- crontab -l
- cat /var/log/cron.log
- service cron status

# .env
- DEBUG=True
- DJANGO_SECRET_KEY=django-insecure-key
- TELEGRAM_TOKEN=token
- TELEGRAM_GROUP_ID=group_id
- POSTGRES_DB=paymentbotdb
- POSTGRES_USER=user
- POSTGRES_PASSWORD=password
- POSTGRES_HOST=db
- POSTGRES_PORT=5432
- PROVIDER_TOKEN=381764678:TEST:118445
- TEST_PROVIDER_TOKEN=381764678:TEST:118445
- CURRENCY=RUB
- PRICE=99000