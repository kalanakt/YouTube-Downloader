<p align="center"><a href="https://thecodexo.com" target="_blank" rel="noopener noreferrer"><img width="250" src="https://github.com/kalanakt/Pyrogram-Telegram-Bot-Template/blob/main/pic/logo_transparent_1100x300.png" alt="Code xo logo"></a></p>

<h2>Thank you for using me 💖. Here are some examples of sending a message via a telegram bot</h2>

<h3>Sending reply text when someone starts the bot.</h3>
<em>If someone starts your bot or sends /start command in chat you can use this to send a reply to it. also, you can use this method for other commands</em>
<br><br>

```
@Client.on_message(filters.command("start"))
async def start(bot, cmd):
```
* <p>You can use filters to identify user commands. </p>

```
@Client.on_message(filters.command("start") & filters.incoming & ~filters.edited & filters.private)
async def start(bot, cmd):
```

* <p>You can also add text to the keyboard. We will talk about that, keep reading ...</p>

```
@Client.on_message(filters.command("start") & filters.private)
async def start(bot, command):
    await command.reply_text(
        text = "Hi {}!, this is wellcom message".format(command.from_user.first_name),
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔮Help", callback_data='help_cb'),
                    InlineKeyboardButton("⚔About", callback_data='about_cb')
                ],
                [
                    InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/kinu6'),
                    InlineKeyboardButton("⚙️Update Channel", url="https://t.me/TMWAD")
                ]
            ]
        )
    )
```

<br><br>
<h3>Sending reply photo with caption when someone starts the bot.</h3>
<em>add your photo url. it should end with .jpg or .jpeg</em>
<br><br>

```
@Client.on_message(filters.command("start") & filters.private)
async def start(bot, command):
    await command.reply_photo(
        photo = "https://telegra.ph/file/adffc5ce502f5578e2806.jpg",
        caption = "Hi {}!, this is wellcom message".format(command.from_user.first_name), 
        disable_web_page_preview=True,
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("🔮Help", callback_data='help_cb'),
                    InlineKeyboardButton("⚔About", callback_data='about_cb')
                ],
                [
                    InlineKeyboardButton("👨🏼‍💻Developer", url='https://t.me/kinu6'),
                    InlineKeyboardButton("⚙️Update Channel", url="https://t.me/TMWAD")
                ]
            ]
        )
    )
    
```

* <p> Check <a href="https://docs.pyrogram.org/api/bound-methods/Message.reply">this</a> For learn more about reply method</p>
