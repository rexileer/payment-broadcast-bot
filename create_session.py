from pyrogram import Client
import os
from dotenv import load_dotenv

load_dotenv(encoding='utf-8')

API_ID = os.getenv('API_ID')
API_HASH = os.getenv('API_HASH')

session_path = "bot/s1_bot" 

app = Client(session_path, api_id=API_ID, api_hash=API_HASH)

app.run()  # Запустит клиент, откроет ввод кода авторизации
