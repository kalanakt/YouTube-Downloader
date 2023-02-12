import os

class Config:
    API_ID = int(os.environ.get("API_ID", ""))
    API_HASH = os.environ.get("API_HASH", "")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "")
    DATABASE_URI = os.environ.get('DATABASE_URI', "")
    DATABASE_NAME = os.environ.get('DATABASE_NAME', "telebot")
