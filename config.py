import os

class Config:
    API_ID = int(os.environ.get("API_ID", "6129651"))
    API_HASH = os.environ.get("API_HASH", "12c5b64ffbd1425f2cf0f2910bc16ef5")
    BOT_TOKEN = os.environ.get("BOT_TOKEN", "6083920856:AAF1p6FXTvl3GDEDNIvOKp4Nhchon6h9sYc")
    DATABASE_URI = os.environ.get('DATABASE_URI', "")
    DATABASE_NAME = os.environ.get('DATABASE_NAME', "telebot")
    OPEN_AI_API_KEY = int(os.environ.get("OPEN_AI_API_KEY", "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"))
