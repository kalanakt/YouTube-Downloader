from config import Config
import asyncio
from pyrogram import Client, idle

async def main():
    TubedroidBot = Client(
        "Tubedroid",
        bot_token=Config.BOT_TOKEN,
        api_id=Config.API_ID,
        api_hash=Config.API_HASH,
        workers=50,
        plugins=dict(root="plugins")
    )

    await TubedroidBot.start()

    await idle()

    await TubedroidBot.stop()


asyncio.run(main())
