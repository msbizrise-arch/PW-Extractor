from config import CHANNEL_ID, SUDO_USERS
from Extractor.core import script
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from Extractor.core.mongo.plans_db import premium_users

async def chk_user(user_id):
    users = await premium_users()
    return 0 if user_id in users or user_id in SUDO_USERS else 1

async def subscribe(app, message):
    if not CHANNEL_ID: return 0
    try:
        user = await app.get_chat_member(CHANNEL_ID, message.from_user.id)
        if user.status in ["kicked", "left"]: raise UserNotParticipant
        return 0
    except UserNotParticipant:
        url = await app.export_chat_invite_link(CHANNEL_ID)
        await message.reply_photo("https://graph.org/file/b7a933f423c153f866699.jpg",
                                  caption=script.FORCE_MSG.format(message.from_user.mention),
                                  reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("Join Channel", url=url)]]))
        return 1
    except:
        return 0

async def get_seconds(time_string):
    # (same as original - fixed parsing)
    value = int(''.join(filter(str.isdigit, time_string)))
    unit = ''.join(filter(str.isalpha, time_string)).lower()
    if unit.startswith('day'): return value * 86400
    if unit.startswith('hour'): return value * 3600
    if unit.startswith('min'): return value * 60
    if unit.startswith('month'): return value * 86400 * 30
    if unit.startswith('year'): return value * 86400 * 365
    return 0
