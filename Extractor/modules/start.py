from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Extractor import app
from Extractor.core.script import START_TXT, IMG
from Extractor.core.func import subscribe, chk_user
from Extractor.modules.pw import pw_mobile, pw_token
from Extractor.modules.plans import *

@app.on_message(filters.command("start"))
async def start(client, message):
    if await subscribe(client, message): return
    await message.reply_photo(IMG[0], caption=START_TXT.format(message.from_user.mention),
                              reply_markup=InlineKeyboardMarkup([
                                  [InlineKeyboardButton("🔥 Physics Wallah", callback_data="pw_")],
                                  [InlineKeyboardButton("💎 My Plan", callback_data="myplan")]
                              ]))

@app.on_callback_query(filters.regex("pw_"))
async def pw_cb(client, query):
    if await chk_user(query, query.from_user.id): return
    await query.message.edit_text("**Choose Login Method**", reply_markup=InlineKeyboardMarkup([
        [InlineKeyboardButton("📱 Mobile + OTP", callback_data="pw_mobile")],
        [InlineKeyboardButton("🔑 Direct Token", callback_data="pw_token")]
    ]))

@app.on_callback_query(filters.regex("pw_mobile"))
async def pw_mobile_cb(client, query):
    await pw_mobile(client, query.message)

@app.on_callback_query(filters.regex("pw_token"))
async def pw_token_cb(client, query):
    await pw_token(client, query.message)
