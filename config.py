import os

class Config:
    API_ID = int(os.environ.get("API_ID", "6129651"))
    API_HASH = os.environ.get("API_HASH", "12c5b64ffbd1425f2cf0f2910bc16ef5")
    BOT_TOKEN = os.environ.get(
        "BOT_TOKEN", "6083920856:AAF1p6FXTvl3GDEDNIvOKp4Nhchon6h9sYc")
