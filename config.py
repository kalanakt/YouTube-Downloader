import os

class Config:
    API_ID = int(os.getenv("API_ID",16789281 ))
    API_HASH = os.getenv("API_HASH", '709ad40f8295b6cc92bf0e2f5fd2ef25')
    BOT_TOKEN = os.getenv("BOT_TOKEN", '6985444142:AAH4XsA_gJdwrk4A9YCLS2QfS9RBy8Sm-qY')
