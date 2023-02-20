# Add bot's callbacks command here

from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery
from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from Script import script
import asyncio
import sys
import ast
import os
import re
from pytube import YouTube, Playlist
from pydub import AudioSegment
import time

from helpers.youtube import get_filetype_keyboard, progress

START_TXT = script.START_TXT
HELP_TXT = script.HELP_TXT
ABOUT_TXT = script.ABOUT_TXT

# Resolution selection handler


@Client.on_callback_query(filters.regex(r'^res_'))
async def select_resolution(client, callback_query):
    # Get the video object from the user's data
    cb_data = callback_query.data.replace('res_', '')
    video_id, cb_resolution = cb_data.split(':')
    youtube = YouTube(f'https://www.youtube.com/watch?v={video_id}')

    formatted_text = callback_query.message.caption
    resolutions = []
    for stream in youtube.streams.filter(progressive=True):
        resolutions.append(stream.resolution)
    buttons = []
    for resolution in resolutions:
        if resolution == cb_resolution:  # check if resolution is cb_resolution
            text = f"{resolution} ✔"
        else:
            text = resolution
        buttons.append(InlineKeyboardButton(
            text=text, callback_data=f"res_{video_id}:{resolution}"))
    # add two new buttons for 'video' and 'audio' in a new row
    cb_t_button = callback_query.message.reply_markup.inline_keyboard[1]
    t_buttons = [
        InlineKeyboardButton(text=button.text, callback_data=button.callback_data) for button in cb_t_button
    ]

    # add a 'download' button in another new row
    cb_d_button = callback_query.message.reply_markup.inline_keyboard[2][0]
    cb_d_button_data = cb_d_button.callback_data.replace('download_', '')
    video_id, c_resolution, c_type = cb_d_button_data.split(':')
    d_buttons = [InlineKeyboardButton(
        text="Download", callback_data=f"download_{video_id}:{cb_resolution}:{c_type}")]

    keyboard = [buttons, t_buttons, d_buttons]
    markup = InlineKeyboardMarkup(keyboard)
    # do something with the callback_data
    return await callback_query.message.edit_reply_markup(reply_markup=markup)
    # youtube = YouTube(f'https://www.youtube.com/watch?v={video_id}')


# File type selection handler
@Client.on_callback_query(filters.regex(r'^type_'))
async def select_file_type(client, callback_query):
    # Get the video object from the user's data
    cb_data = callback_query.data.replace('type_', '')
    video_id, cb_type = cb_data.split(':')
    formatted_text = callback_query.message.caption
    t_buttons = [
        InlineKeyboardButton(text="Video ✔" if cb_type == 'video' else "Video",
                             callback_data=f"type_{video_id}:video"),
        InlineKeyboardButton(text="Audio ✔" if cb_type == 'audio' else "Audio",
                             callback_data=f"type_{video_id}:audio")
    ]

    cb_res_button = callback_query.message.reply_markup.inline_keyboard[0]

    buttons = [
        InlineKeyboardButton(text=button.text, callback_data=button.callback_data) for button in cb_res_button
    ]

    cb_d_button = callback_query.message.reply_markup.inline_keyboard[2][0]
    cb_d_button_data = cb_d_button.callback_data.replace('download_', '')
    video_id, c_resolution, c_type = cb_d_button_data.split(':')
    d_buttons = [InlineKeyboardButton(
        text="Download", callback_data=f"download_{video_id}:{c_resolution}:{cb_type}")]

    keyboard = [buttons, t_buttons, d_buttons]
    markup = InlineKeyboardMarkup(keyboard)
    # do something with the callback_data
    return await callback_query.message.edit_reply_markup(reply_markup=markup)


@Client.on_callback_query(filters.regex(r'^download_'))
async def download(client, callback_query):
    # Get the video object from the user's data
    cb_data = callback_query.data.replace('download_', '')
    video_id, c_resolution, c_type = cb_data.split(':')
    youtube = YouTube(f'https://www.youtube.com/watch?v={video_id}')
    title = youtube.title
    thumbnail_url = youtube.thumbnail_url
    description = youtube.description
    formatted_text = f"<b>{title}</b>\n\n{description[:300]}{'...' if len(description) > 300 else ''} \n\n<b>Powerd By: @TMWAD With <a href='https://t.me/videoDefUserBot''>@videoDefUserBot</a></b>."
    # Get a list of all streams for the video
    # Replace | with -
    file_name = f"{youtube.title} - {youtube.author}".replace("|", "-")
    if c_resolution == 'n' and c_type == 'n':
        extensions = []

        for stream in youtube.streams:
            mime_type = stream.mime_type
            extension = mime_type.split('/')[-1]
            extensions.append(extension)

        if len(extensions) == 1:
            filetype = extensions[0]
        elif 'mp4' in extensions:
            filetype = 'mp4'
        else:
            filetype = extensions[0]

        video = youtube.streams.filter(
            res='720p', file_extension=filetype, progressive=True).first()
        if video is not None:
            video.download(filename=f"{file_name}.{filetype}")
        else:
            return await callback_query.answer("Please Choice Another resolution. your decied resolution is not available", show_alert=True)
        # Send the downloaded video to the user
        await client.send_video(
            chat_id=callback_query.message.chat.id,
            video=open(f'{file_name}.{filetype}', 'rb'),
            caption=formatted_text,
            parse_mode=ParseMode.HTML,
            progress=progress,
        )

        if os.path.exists(f'{file_name}.mp4'):
            os.remove(f'{file_name}.mp4')

    elif c_type == 'video' and c_type == 'n':
        extensions = []

        for stream in youtube.streams:
            mime_type = stream.mime_type
            extension = mime_type.split('/')[-1]
            extensions.append(extension)

        if len(extensions) == 1:
            filetype = extensions[0]
        elif 'mp4' in extensions:
            filetype = 'mp4'
        else:
            filetype = extensions[0]

        video = youtube.streams.filter(
            res='720p', file_extension=filetype, progressive=True).first()
        if video is not None:
            video.download(filename=f"{file_name}.{filetype}")
        else:
            return await callback_query.answer("Please Choice Another resolution. your decied resolution is not available", show_alert=True)
        # Send the downloaded video to the user
        await client.send_video(
            chat_id=callback_query.message.chat.id,
            video=open(f'{file_name}.{filetype}', 'rb'),
            caption=formatted_text,
            parse_mode=ParseMode.HTML,
            progress=progress,
        )
        if os.path.exists(f'{file_name}.mp4'):
            os.remove(f'{file_name}.mp4')

    elif c_type == 'video' and c_type != 'n':
        extensions = []

        for stream in youtube.streams:
            mime_type = stream.mime_type
            extension = mime_type.split('/')[-1]
            extensions.append(extension)

        if len(extensions) == 1:
            filetype = extensions[0]
        elif 'mp4' in extensions:
            filetype = 'mp4'
        else:
            filetype = extensions[0]

        video = youtube.streams.filter(
            res=c_resolution, file_extension=filetype, progressive=True).first()
        if video is not None:
            video.download(filename=f"{file_name}.{filetype}")
        else:
            return await callback_query.answer("Please Choice Another resolution. your decied resolution is not available", show_alert=True)
        # Send the downloaded video to the user
        await client.send_video(
            chat_id=callback_query.message.chat.id,
            video=open(f'{file_name}.{filetype}', 'rb'),
            caption=formatted_text,
            parse_mode=ParseMode.HTML,
            progress=progress,
        )
        if os.path.exists(f'{file_name}.mp4'):
            os.remove(f'{file_name}.mp4')

    elif c_type == 'audio':
        audio_streams = youtube.streams.filter(
            res=c_resolution,file_extension='mp4', progressive=True).first()
        if audio_streams is not None:
            audio_file = audio_streams.download(filename=file_name)
        else:
            return await callback_query.answer("Audio File is not availbe for this link!", show_alert=True)
        # Send the downloaded video to the user
        # Create an audio segment from the downloaded file
        audio_segment = AudioSegment.from_file(audio_file)
        mp3_file = audio_file[:-3] + 'mp3'
        audio_segment.export(mp3_file, format='mp3')

        # Delete the original audio file
        try:
            await client.send_audio(
                chat_id=callback_query.message.chat.id,
                audio=open(f'{file_name}.mp3', 'rb'),
                caption=formatted_text,
                parse_mode=ParseMode.HTML,
                progress=progress,
            )
        except Exception as e:
            return await client.send_message(callback_query.message.chat.id, f"Error {e}")

        if os.path.exists(f'{file_name}.mp3'):
            os.remove(f'{file_name}.mp3')
        if os.path.exists(f'{file_name}.mp4'):
            os.remove(f'{file_name}.mp4')


@Client.on_callback_query(filters.regex(r'^pl_res_'))
async def pl_select_resolution(client, callback_query):
    cb_data = callback_query.data.replace('pl_res_', '')
    playlist_id, cb_resolution = cb_data.split(':')

    formatted_text = callback_query.message.text

    resolutions = ['360p', '480p', '720p']
    buttons = []
    for resolution in resolutions:
        if resolution == cb_resolution:  # check if resolution is cb_resolution
            text = f"{resolution} ✔"
        else:
            text = resolution
        buttons.append(InlineKeyboardButton(
            text=text, callback_data=f"pl_res_{playlist_id}:{resolution}"))

    cb_t_button = callback_query.message.reply_markup.inline_keyboard[1]
    t_buttons = [
        InlineKeyboardButton(text=button.text, callback_data=button.callback_data) for button in cb_t_button
    ]

    cb_d_button = callback_query.message.reply_markup.inline_keyboard[2][0]
    cb_d_button_data = cb_d_button.callback_data.replace('pl_download_', '')
    playlist_id, c_resolution, c_type = cb_d_button_data.split(':')
    d_buttons = [InlineKeyboardButton(
        text="Download", callback_data=f"pl_download_{playlist_id}:{cb_resolution}:{c_type}")]

    keyboard = [buttons, t_buttons, d_buttons]
    markup = InlineKeyboardMarkup(keyboard)
    # do something with the callback_data
    return await callback_query.message.edit_reply_markup(reply_markup=markup)


@Client.on_callback_query(filters.regex(r'^pl_type_'))
async def pl_select_file_type(client, callback_query):
    cb_data = callback_query.data.replace('pl_type_', '')
    playlist_id, cb_type = cb_data.split(':')

    formatted_text = callback_query.message.text

    cb_res_button = callback_query.message.reply_markup.inline_keyboard[0]
    buttons = [
        InlineKeyboardButton(text=button.text, callback_data=button.callback_data) for button in cb_res_button
    ]

    t_buttons = [
        InlineKeyboardButton(text="Video ✔" if cb_type == 'video' else "Video",
                             callback_data=f"pl_type_{playlist_id}:video"),
        InlineKeyboardButton(text="Audio ✔" if cb_type == 'audio' else "Audio",
                             callback_data=f"pl_type_{playlist_id}:audio")
    ]

    cb_d_button = callback_query.message.reply_markup.inline_keyboard[2][0]
    cb_d_button_data = cb_d_button.callback_data.replace('pl_download_', '')
    video_id, c_resolution, c_type = cb_d_button_data.split(':')
    d_buttons = [InlineKeyboardButton(
        text="Download", callback_data=f"pl_download_{playlist_id}:{c_resolution}:{cb_type}")]

    keyboard = [buttons, t_buttons, d_buttons]
    markup = InlineKeyboardMarkup(keyboard)
    # do something with the callback_data
    return await callback_query.message.edit_reply_markup(reply_markup=markup)


@Client.on_callback_query(filters.regex(r'^pl_download_'))
async def pl_download(client, callback_query):
    cb_data = callback_query.data.replace('pl_download_', '')
    playlist_id, c_resolution, c_type = cb_data.split(':')
    playlist_url = f"https://youtube.com/playlist?list={playlist_id}"
    playlist = Playlist(playlist_url)
    playlist_title = playlist.title
    final_text = f"Playlist <b>{playlist_title}</b> has been downloaded and uploaded! \n\n<b>Powerd By: @TMWAD With <a href='https://t.me/videoDefUserBot''>@videoDefUserBot</a></b>."

    try:
        for video in playlist.videos:
            thumbnail_url = video.thumbnail_url
            title = video.title
            description = video.description
            author = video.author
            confirm_text = f"Downloading video <b>{title} ...</b>"
            formatted_text = f"<b>{title}</b>\n\n{description[:300]}{'...' if len(description) > 300 else ''}"
            try:
                k = await client.send_photo(
                    chat_id = callback_query.message.chat.id,
                    photo=thumbnail_url,
                    caption=confirm_text,
                    parse_mode=ParseMode.HTML)
            except Exception as e:
                k = await bot.send_message(chat_id, formatted_text)

            file_name = f"{title} - {author}".replace("|", "-")
            yt_video = video.streams.filter(res=c_resolution, file_extension='mp4', progressive=True).first()

            if yt_video is not None:
                yt_video.download(filename=f"{file_name}.mp4", output_path="./videos")
            else:
                await client.send_message(callback_query.message.chat.id, f"Video Not Availe For Selected Resolution. Change The resolution and try again.")

            video_path = f"./videos/{file_name}.mp4"
            with open(video_path, "rb") as f:
                await client.send_video(
                    chat_id=callback_query.message.chat.id,
                    video=video_path,
                    caption=formatted_text,
                    parse_mode=ParseMode.HTML,
                    progress=progress,
                )
            k.delete()
            if os.path.exists(video_path):
                os.remove(video_path)
            time.sleep(30)

        await client.send_message(callback_query.message.chat.id, final_text)
    except Exception as e:
        await client.send_message(callback_query.message.chat.id, f"Error: {e}")

@Client.on_callback_query()
async def cb_handler(client: Client, query: CallbackQuery):
    if query.data == "help_cb":
        buttons = [
            [
                InlineKeyboardButton("⚔About", callback_data='about_cb'),
                InlineKeyboardButton("⚡Back", callback_data='start_cb')
            ],
            [
                InlineKeyboardButton(
                    "👨🏼‍💻Developer", url='https://t.me/kinu6'),
                InlineKeyboardButton("⚙️Update Channel",
                                     url="https://t.me/TMWAD")
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
                InlineKeyboardButton(
                    "👨🏼‍💻Developer", url='https://t.me/kinu6'),
                InlineKeyboardButton("⚙️Update Channel",
                                     url="https://t.me/TMWAD")
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
                InlineKeyboardButton(
                    "👨🏼‍💻Developer", url='https://t.me/kinu6'),
                InlineKeyboardButton("⚙️Update Channel",
                                     url="https://t.me/TMWAD")
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
