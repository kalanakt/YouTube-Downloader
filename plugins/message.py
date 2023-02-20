from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from Script import script
import asyncio
import sys
import os
import re
from pytube import YouTube, Playlist

from helpers.database import u_video
from helpers.youtube import get_resolution_keyboard, get_youtube_video_id


START_TXT = script.START_TXT
HELP_TXT = script.HELP_TXT
ABOUT_TXT = script.ABOUT_TXT


@Client.on_message(filters.regex(r'https?:\/\/(?:www\.)?(?:m\.)?(?:youtube\.com|youtu\.be)\/(?:watch\?v=)?([a-zA-Z0-9_-]{11})$'))
async def handle_youtube_link(bot, message):
    video_id = get_youtube_video_id(message.text)
    youtube = YouTube(f'https://www.youtube.com/watch?v={video_id}')
    thumbnail_url = youtube.thumbnail_url
    title = youtube.title
    description = youtube.description
    formatted_text = f"<b>{title}</b>\n\n{description[:300]}{'...' if len(description) > 300 else ''} <a href='https://www.youtube.com/watch?v={video_id}''>Read more</a>\n\n\nOnly download videos that you have the right to download. Do not use this bot to download copyrighted content that you do not have permission to use.\nDo not use this bot to download content that is illegal or violates Telegram's terms of service.\nBe respectful to other users and do not use the bot to spam or harass others.\nThe bot can only download videos that are publicly available on YouTube.\nThe bot can only download videos up to a maximum file size of 2 GB.\nThe bot can only download videos that are available in a format that can be downloaded."
    resolutions = []

    try:
        for stream in youtube.streams.filter(progressive=True):
            resolutions.append(stream.resolution)
        buttons = [
            InlineKeyboardButton(text=resolution, callback_data=f"res_{video_id}:{resolution}") for resolution in resolutions
        ]
        # add two new buttons for 'video' and 'audio' in a new row
        t_buttons = []

        t_buttons.append(InlineKeyboardButton(
            text="Video", callback_data=f"type_{video_id}:video"))
        t_buttons.append(InlineKeyboardButton(
            text="Audio", callback_data=f"type_{video_id}:audio"))

        # add a 'download' button in another new row
        d_buttons = [InlineKeyboardButton(
            text="Download", callback_data=f"download_{video_id}:n:n")]
        keyboard = [buttons, t_buttons, d_buttons]
        markup = InlineKeyboardMarkup(keyboard)
        await message.reply_photo(
            photo=thumbnail_url,
            caption=formatted_text,
            parse_mode=ParseMode.HTML,
            reply_markup=markup)
    except Exception as e:
        await bot.send_message(message.chat.id, f"Error: {e}")

@Client.on_message(filters.regex(r"(?:(?:https?:)?//)?(?:www\.)?youtube\.com/playlist\?list=([a-zA-Z0-9_-]+)"))
async def handle_youtube_playlist_link(bot, message):
    try:
        playlist_url = message.text
        chat_id = message.chat.id
        match = re.search(r"list=([A-Za-z0-9_-]+)", playlist_url)
        if match:
            playlist_id = match.group(1)
        else:
            return await bot.send_message(chat_id, 'Something went wrong; Youtube Link Not Found!')

        playlist = Playlist(playlist_url)
        playlist_title = playlist.title

        formatted_text = f"<b>Playlist: {playlist_title}</b>\n\nOnly download videos that you have the right to download. Do not use this bot to download copyrighted content that you do not have permission to use.\nDo not use this bot to download content that is illegal or violates Telegram's terms of service.\nBe respectful to other users and do not use the bot to spam or harass others.\nThe bot can only download videos that are publicly available on YouTube.\nThe bot can only download videos up to a maximum file size of 2 GB.\nThe bot can only download videos that are available in a format that can be downloaded."

        resolutions = ['360p', '480p', '720p']
        buttons = [
            InlineKeyboardButton(text=resolution, callback_data=f"pl_res_{playlist_id}:{resolution}") for resolution in resolutions
        ]

        t_buttons = []
        t_buttons.append(InlineKeyboardButton(
            text="Video", callback_data=f"pl_type_{playlist_id}:video"))
        t_buttons.append(InlineKeyboardButton(
            text="Audio", callback_data=f"pl_type_{playlist_id}:audio"))

        d_buttons = [InlineKeyboardButton(
            text="Download", callback_data=f"pl_download_{playlist_id}:n:n")]

        keyboard = [buttons, t_buttons, d_buttons]
        markup = InlineKeyboardMarkup(keyboard)

        await bot.send_message(chat_id=chat_id, text=formatted_text ,reply_markup=markup)

    except Exception as e:
        await bot.send_message(message.chat.id, f"Error: {e}")
