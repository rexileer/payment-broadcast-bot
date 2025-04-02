FROM python:3.13

WORKDIR /app

# Копируем файл зависимостей и устанавливаем их
COPY requirements.txt /app/
RUN pip install -r requirements.txt

# Устанавливаем cron
RUN apt-get update && apt-get install -y cron

# Копируем все файлы проекта
COPY . /app/

# Копируем файл с cron-задачей и настраиваем crontab
COPY mycron /etc/cron.d/mycron
RUN chmod 0644 /etc/cron.d/mycron && crontab /etc/cron.d/mycron

EXPOSE 8000

# По умолчанию для веб-приложения запускается gunicorn (можно переопределять через docker-compose)
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "core.wsgi:application"]
