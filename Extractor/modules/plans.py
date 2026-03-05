from datetime import timedelta
import pytz
import datetime
from Extractor import app
from config import SUDO_USERS, PREMIUM_LOGS, OWNER_ID
from Extractor.core.func import get_seconds
from Extractor.core.mongo.plans_db import add_premium, remove_premium, check_premium, premium_users
from pyrogram import filters
from pyrogram.errors.exceptions.bad_request_400 import MessageTooLong
from pyrogram.types import Message

@app.on_message(filters.command("remove_premium") & filters.user(SUDO_USERS))
async def remove_premium_cmd(client, message: Message):
    if len(message.command) != 2:
        await message.reply_text("ᴜꜱᴀɢᴇ : /remove_premium user_id")
        return

    try:
        user_id = int(message.command[1])
    except ValueError:
        await message.reply_text("Invalid user ID – must be a number")
        return

    user = await client.get_users(user_id)
    data = await check_premium(user_id)

    if data:
        await remove_premium(user_id)
        await message.reply_text("ᴜꜱᴇʀ ʀᴇᴍᴏᴠᴇᴅ ꜱᴜᴄᴄᴇꜱꜱꜰᴜʟʟʏ !")
        await client.send_message(
            chat_id=user_id,
            text=f"<b>Hey {user.mention},\n\nYour premium access has been removed.\nThank you for using our service 😊.</b>"
        )
    else:
        await message.reply_text("ɴᴏ ᴘʀᴇᴍɪᴜᴍ ᴅᴀᴛᴀ ғᴏᴜɴᴅ ғᴏʀ ᴛʜɪs ᴜsᴇʀ !")

# ... (rest of myplan_cmd, chk_premium_cmd, add_premium_cmd same as fetched, but add <code>{user_id}</code> in text where missing)

@app.on_message(filters.command("myplan"))
async def myplan_cmd(client, message: Message):
    user_id = message.from_user.id
    user_mention = message.from_user.mention
    data = await check_premium(user_id)

    if not data or "expire_date" not in data:
        await message.reply_text(f"ʜᴇʏ {user_mention},\n\nʏᴏᴜ ᴅᴏ ɴᴏᴛ ʜᴀᴠᴇ ᴀɴʏ ᴀᴄᴛɪᴠᴇ ᴘʀᴇᴍɪᴜᴍ ᴘʟᴀɴs")
        return

    expiry = data["expire_date"]
    tz = pytz.timezone("Asia/Kolkata")
    expiry_ist = expiry.astimezone(tz)
    expiry_str = expiry_ist.strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")

    now_ist = datetime.datetime.now(tz)
    time_left = expiry_ist - now_ist

    if time_left.total_seconds() <= 0:
        await message.reply_text(f"ʜᴇʏ {user_mention},\n\nʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ʜᴀs ᴇxᴘɪʀᴇᴅ !")
        await remove_premium(user_id)
        return

    days = time_left.days
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    time_left_str = f"{days} ᴅᴀʏꜱ, {hours} ʜᴏᴜʀꜱ, {minutes} ᴍɪɴᴜᴛᴇꜱ"
    await message.reply_text(
        f"⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :\n\n"
        f"👤 ᴜꜱᴇʀ : {user_mention}\n"
        f"⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n"  # Fixed
        f"⏰ ᴛɪᴍᴇ ʟᴇғᴛ : {time_left_str}\n"
        f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str}"
    )

# Similar fixes for chk_premium_cmd and add_premium_cmd – add <code>{user_id}</code>

# (Full code with fixes – paste the entire fetched code but with <code> added to user_id lines)
