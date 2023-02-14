from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from pyrogram import Client, filters
from Script import script
import asyncio
import sys
import os
import re
import shutil
import requests
from pytube import YouTube

from helpers.youtube import get_resolution_keyboard

START_TXT = script.START_TXT
HELP_TXT = script.HELP_TXT
ABOUT_TXT = script.ABOUT_TXT


@Client.on_message(filters.regex(r'https?:\/\/(?:www\.)?(?:m\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?([a-zA-Z0-9_-]{11})$'))
async def download_video(client, message):
    # Create a YouTube object
    video_url = message.text
    video = YouTube(video_url)

    # Ask the user for the resolution and file type
    await message.reply_text(
        f"Video title: {video.title}\n"
        "What resolution do you want to download it in?",
        reply_markup=get_resolution_keyboard(video)
    )

    # Store the video object in the user's data for later use
    await Client.storage.set("video_data:" + str(message.chat.id), video)
