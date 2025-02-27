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


@bot.on_inline_query()
async def inlinequery(client, inline_query):
    answer = []
    if inline_query.query == "":
        await inline_query.answer(
            results=[

                InlineQueryResultArticle(
                    title="ʟʏʀɪᴄꜱ ᴋᴇ ʟɪʏᴇ ꜱᴇᴀʀᴄʜ ᴋᴀʀᴏ...",
                    description="Lyrics bot",
                    reply_markup=InlineKeyboardMarkup(
                        [
                            [
                                InlineKeyboardButton("🔍ʟʏʀɪᴄꜱ ᴋᴇ ʟɪʏᴇ ꜱᴇᴀʀᴄʜ ᴋᴀʀᴏ..", switch_inline_query_current_chat="")
                            ]
                        ]
                    ),
                    input_message_content=InputTextMessageContent(
                        "Search for lyrics inline..."
                    )
                )
            ]
        )
    else:
        INLINE_SONG = inline_query.query
        print(INLINE_SONG)
        INLINE_LYRICS = GENIUS.search_song(INLINE_SONG)
        INLINE_TITLE = INLINE_LYRICS.title
        INLINE_ARTISTE = INLINE_LYRICS.artist
        INLINE_TEXT = INLINE_LYRICS.lyrics
        answer.append(
            InlineQueryResultArticle(
                title=INLINE_TITLE,
                description=INLINE_ARTISTE,
                reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("ᴡʀᴏɴɢ ʀᴇꜱᴜʟᴛ?", switch_inline_query_current_chat=INLINE_SONG),
                            InlineKeyboardButton("🔍ꜰɪʀ ꜱᴇ ꜱᴇᴀʀᴄʜ ᴋɪᴊɪʏᴇ ɴᴀ..", switch_inline_query_current_chat="")
                        ]
                    ]
                ),
                input_message_content=InputTextMessageContent(f"**мυנнє ує мιℓα...**\n\n🎶Name: **{INLINE_TITLE}**\n🎙️Artiste: **{INLINE_ARTISTE}**\n\n`{INLINE_TEXT}`")
            )
        )
    await inline_query.answer(
        results=answer,
        cache_time=1
    )


print("𝙰𝙱𝙷𝙸 𝙻𝚈𝚁𝙸𝙲𝚂 𝙱𝙾𝚃 𝙲𝙷𝙰𝙻𝚄 𝙷𝙾 𝙶𝙰𝚈𝙰 𝙷𝙰𝙸")
bot.run()
