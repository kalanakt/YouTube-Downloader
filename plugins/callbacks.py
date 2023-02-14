# Add bot's callbacks command here

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import Client, filters
from Script import script
import asyncio
import sys
import ast
import os
import re

from helpers.youtube import get_filetype_keyboard

START_TXT = script.START_TXT
HELP_TXT = script.HELP_TXT 
ABOUT_TXT = script.ABOUT_TXT

# Resolution selection handler
@Client.on_callback_query(filters.regex(r'^res_'))
async def select_resolution(client, callback_query):
    # Get the video object from the user's data
    video = await Client.storage.get("video_data:" + str(callback_query.message.chat.id))

    # Extract the selected resolution from the callback data
    resolution = int(re.search(r'^res_(\d+)$', callback_query.data).group(1))

    # Ask the user for the file type
    await callback_query.message.edit_text(
        "What file type do you want to download it as?",
        reply_markup=get_filetype_keyboard(video, resolution)
    )

    # Store the resolution in the user's data for later use
    await Client.storage.set("video_resolution:" + str(callback_query.message.chat.id), resolution)

# File type selection handler
@Client.on_callback_query(filters.regex(r'^filetype_'))
async def select_filetype(client, callback_query):
    # Get the video object and resolution from the user's data
    video = await Client.storage.get("video_data:" + str(callback_query.message.chat.id))
    resolution = await Client.storage.get("video_resolution:" + str(callback_query.message.chat.id))

    # Extract the selected file type from the callback data
    filetype = re.search(r'^filetype_(.*)$', callback_query.data).group(1)

    # Download the selected stream
    stream = video.streams.filter(res=f"{resolution}p", file_extension=filetype).first()
    stream.download()

    # Convert the downloaded video to MP4
    file_title = video.title.replace(" ", "_")
    old_file_path = f"{stream.default_filename}"
    new_file_path = f"{file_title}.{filetype}"
    os.rename(old_file_path, new_file_path)

    # Upload the converted video to Box


@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "help_cb":
        buttons = [
          [
            InlineKeyboardButton("⚔About", callback_data='about_cb'),
            InlineKeyboardButton("⚡Back", callback_data='start_cb')
          ],
          [
            InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/kinu6'),
            InlineKeyboardButton("⚙️Update Channel", url="https://t.me/TMWAD")
          ],
          [
            InlineKeyboardButton("🧿Close", callback_data='close')
          ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=HELP_TXT,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    
    elif query.data == "about_cb":
        buttons = [
          [
            InlineKeyboardButton("🔮Help", callback_data='help_cb'),
            InlineKeyboardButton("⚡Back", callback_data='start_cb')
          ],
          [
            InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/kinu6'),
            InlineKeyboardButton("⚙️Update Channel", url="https://t.me/TMWAD")
          ],
          [
            InlineKeyboardButton("🧿Close", callback_data='close')
          ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=ABOUT_TXT,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
    
    elif query.data == "start_cb":
        buttons = [
          [
            InlineKeyboardButton("🔮Help", callback_data='help_cb'),
            InlineKeyboardButton("⚔About", callback_data='about_cb')
          ],
          [
            InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/kinu6'),
            InlineKeyboardButton("⚙️Update Channel", url="https://t.me/TMWAD")
          ]
        ]
        reply_markup = InlineKeyboardMarkup(buttons)
        await query.message.edit_text(
            text=START_TXT,
            reply_markup=reply_markup,
            disable_web_page_preview=True
        )
        
    elif query.data == "close":
        await query.message.delete()
