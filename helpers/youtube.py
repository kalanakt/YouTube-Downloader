from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_youtube_video_id(url):
    """Extracts the video ID from a YouTube URL"""
    video_id = None
    if 'youtube.com' in url:
        video_id = url.split('v=')[-1]
        if '&' in video_id:
            video_id = video_id.split('&')[0]
    elif 'youtu.be' in url:
        video_id = url.split('/')[-1]
    return video_id

def get_resolution_keyboard(video):
    resolutions = {}
    for stream in video.streams.filter(progressive=True):
        resolution = stream.resolution or "Audio Only"
        resolutions[resolution] = stream.itag

    keyboard = []
    for resolution, itag in resolutions.items():
        callback_data = f"res_{itag}"
        button = InlineKeyboardButton(resolution, callback_data=callback_data)
        keyboard.append([button])

    return InlineKeyboardMarkup(keyboard)


def get_filetype_keyboard(video, resolution):
    stream = video.streams.filter(res=f"{resolution}p", file_extension="mp4").first()
    filetypes = ["mp4", "webm"]
    if stream and stream.is_progressive:
        filetypes.append("3gp")

    buttons = [
        InlineKeyboardButton(filetype.upper(), callback_data=f"filetype_{filetype}")
        for filetype in filetypes
    ]
    keyboard = InlineKeyboardMarkup([buttons])

    return keyboard

async def progress(current, total):
    print(f"{current * 100 / total:.1f}%")