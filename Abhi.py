import os
import lyricsgenius
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, InlineQueryResultArticle, InputTextMessageContent
from requests.exceptions import Timeout, HTTPError
from pyrogram.errors import MessageTooLong
from Config import Config

bot = Client(
    "bot",
    api_id=Config.API_ID,
    api_hash=Config.API_HASH,
    bot_token=Config.BOT_TOKEN
)

GENIUS = lyricsgenius.Genius(Config.TOKEN)


@bot.on_message(filters.command("start") & filters.private)
async def start(bot, message):
    await bot.send_message(message.chat.id, f"Hҽʅʅσ **{message.from_user.first_name}**!!\n\nᴡᴇʟᴄᴏᴍᴇ ᴛᴏ ᴀʙʜɪ ʟʏʀɪᴄꜱ ʙᴏᴛ."
                                            f"ʏᴏᴜ ᴄᴀɴ ɢᴇᴛ ʟʏʀɪᴄꜱ ᴏꜰ ᴀɴʏ ꜱᴏɴɢ ᴡʜɪᴄʜ ɪꜱ ᴏɴ ɢᴇɴɪᴜꜱ.ᴄᴏᴍ ᴜꜱɪɴɢ ᴛʜɪꜱ ʙᴏᴛ. ᴊᴜꜱᴛ"
                                            f"ꜱᴇɴᴅ ᴛʜᴇ ɴᴀᴍᴇ ᴏꜰ ᴛʜᴇ ꜱᴏɴɢ ᴛʜᴀᴛ ʏᴏᴜ ᴡᴀɴᴛ ᴛᴏ ɢᴇᴛ ʟʏʀɪᴄꜱ. ᴛʜɪꜱ ɪꜱ"
                                            f"Qᴜɪᴛᴇ ꜱɪᴍᴘʟᴇ.", reply_markup=InlineKeyboardMarkup(
        [
            [
                InlineKeyboardButton("🔍ʀᴜᴋᴏ ᴀʙʜɪ ʟʏʀɪᴄꜱ ᴅʜᴜɴᴅʜ ʀᴀʜᴀ ʜᴜ...", switch_inline_query_current_chat="")
            ]
        ]
    ))
  

@bot.on_message(filters.text & filters.private)
async def lyric_get(bot, message):
    try:
        m = await message.reply(
            "🔍ʀᴜᴋᴏ ᴀʙʜɪ ʟʏʀɪᴄꜱ ᴅʜᴜɴᴅʜ ʀᴀʜᴀ ʜᴜ..."
        )
        song_name = message.text
        LYRICS = GENIUS.search_song(song_name)
        if LYRICS is None:
            await m.edit_text(
                "  🎀  𝒦♡𝒾 𝐿𝓎𝓇𝒾𝒸𝓈 𝒩𝒶𝒽𝒾 𝑀𝒾𝓁𝒶  🍬"
            )
        global TITLE
        global ARTISTE
        global TEXT
        TITLE = LYRICS.title
        ARTISTE = LYRICS.artist
        TEXT = LYRICS.lyrics
    except Timeout:
        pass
    except HTTPError as https_e:
        print(https_e)
    try:
        await m.edit_text(
            f"🎶𝒢𝒶𝒶𝓃𝑒 𝒦𝒶 𝒩𝒶𝒶𝓂: **{TITLE}**\n🎙️Artiste: **{ARTISTE}**\n\n`{TEXT}`", reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔍ʀᴜᴋᴏ ᴀʙʜɪ ʟʏʀɪᴄꜱ ᴅʜᴜɴᴅʜ ʀᴀʜᴀ ʜᴜ...", switch_inline_query_current_chat="")
                    ]
                ]
            )
        )
    except MessageTooLong:
        with open(f'downloads/{TITLE}.txt', 'w') as file:
            file.write(f'{TITLE}\n{ARTISTE}\n\n{TEXT}')
            await m.edit_text(
                "ʟʏʀɪᴄꜱ ʟᴀᴍʙɪ ʜᴀɪ ɪꜱʟɪʏᴇ ᴛᴇxᴛ ꜰɪʟᴇ ᴍᴇ ʙʜᴇᴊ ʀᴀʜᴀ ʜᴜ..."
            )
            await bot.send_document(message.chat.id, document=f'downloads/{TITLE}.txt', caption=f'\n{TITLE}\n{ARTISTE}')
            os.remove(f'downloads/{TITLE}.txt')
