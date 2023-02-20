from pyrogram.raw import functions, types
from pyrogram import Client, idle
from config import Config

bot = Client(
    "bot",
    bot_token=Config.BOT_TOKEN,
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    workers=50,
    plugins=dict(root="plugins")
)
bot.start()
print("Bot Started ⚡")
idle()
bot.stop()
