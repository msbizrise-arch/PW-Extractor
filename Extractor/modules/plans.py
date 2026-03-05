from datetime import timedelta
import pytz
import datetime
from Extractor import app
from config import SUDO_USERS, PREMIUM_LOGS, OWNER_ID
from Extractor.core.func import get_seconds
# Fixed import - use named imports instead of *
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
            text=f"<b>ʜᴇʏ {user.mention},\n\nʏᴏᴜʀ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇss ʜᴀs ʙᴇᴇɴ ʀᴇᴍᴏᴠᴇᴅ.\nᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴜsɪɴɢ ᴏᴜʀ sᴇʀᴠɪᴄᴇ 😊.</b>"
        )
    else:
        await message.reply_text("ɴᴏ ᴘʀᴇᴍɪᴜᴍ ᴅᴀᴛᴀ ғᴏᴜɴᴅ ғᴏʀ ᴛʜɪs ᴜsᴇʀ !")


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
        await remove_premium(user_id)  # optional cleanup
        return

    days = time_left.days
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    time_left_str = f"{days} ᴅᴀʏꜱ, {hours} ʜᴏᴜʀꜱ, {minutes} ᴍɪɴᴜᴛᴇꜱ"
    await message.reply_text(
        f"⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :\n\n"
        f"👤 ᴜꜱᴇʀ : {user_mention}\n"
        f"⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n"
        f"⏰ ᴛɪᴍᴇ ʟᴇғᴛ : {time_left_str}\n"
        f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str}"
    )


@app.on_message(filters.command("chk_premium") & filters.user(SUDO_USERS))
async def chk_premium_cmd(client, message: Message):
    if len(message.command) != 2:
        await message.reply_text("ᴜꜱᴀɢᴇ : /chk_premium user_id")
        return

    try:
        user_id = int(message.command[1])
    except ValueError:
        await message.reply_text("Invalid user ID")
        return

    user = await client.get_users(user_id)
    data = await check_premium(user_id)

    if not data or "expire_date" not in data:
        await message.reply_text("ɴᴏ ᴘʀᴇᴍɪᴜᴍ ᴅᴀᴛᴀ ғᴏᴜɴᴅ !")
        return

    expiry = data["expire_date"]
    tz = pytz.timezone("Asia/Kolkata")
    expiry_ist = expiry.astimezone(tz)
    expiry_str = expiry_ist.strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")

    now_ist = datetime.datetime.now(tz)
    time_left = expiry_ist - now_ist

    days = time_left.days
    hours, remainder = divmod(time_left.seconds, 3600)
    minutes, _ = divmod(remainder, 60)

    time_left_str = f"{days} days, {hours} hours, {minutes} minutes"
    await message.reply_text(
        f"⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀ ᴅᴀᴛᴀ :\n\n"
        f"👤 ᴜꜱᴇʀ : {user.mention}\n"
        f"⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n"
        f"⏰ ᴛɪᴍᴇ ʟᴇғᴛ : {time_left_str}\n"
        f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str}"
    )


@app.on_message(filters.command("add_premium") & filters.user(SUDO_USERS))
async def add_premium_cmd(client, message: Message):
    if len(message.command) != 4:
        await message.reply_text(
            "ᴜꜱᴀɢᴇ : /add_premium user_id amount unit\n"
            "Example: /add_premium 123456789 30 day"
        )
        return

    try:
        user_id = int(message.command[1])
        amount = int(message.command[2])
        unit = message.command[3].lower()
    except ValueError:
        await message.reply_text("Invalid format – user_id must be number, amount must be number")
        return

    seconds = await get_seconds(f"{amount} {unit}")
    if seconds <= 0:
        await message.reply_text(
            "Invalid time unit. Use: day, hour, min, month, year"
        )
        return

    user = await client.get_users(user_id)
    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.datetime.now(tz)
    expiry = now + timedelta(seconds=seconds)
    expiry_str = expiry.strftime("%d-%m-%Y\n⏱️ ᴇxᴘɪʀʏ ᴛɪᴍᴇ : %I:%M:%S %p")
    join_str = now.strftime("%d-%m-%Y\n⏱️ ᴊᴏɪɴɪɴɢ ᴛɪᴍᴇ : %I:%M:%S %p")

    await add_premium(user_id, expiry)

    await message.reply_text(
        f"ᴘʀᴇᴍɪᴜᴍ ᴀᴅᴅᴇᴅ ꜱᴜᴄᴄᴇꜱꜱғᴜʟʟʏ ✅\n\n"
        f"👤 ᴜꜱᴇʀ : {user.mention}\n"
        f"⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n"
        f"⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : {amount} {unit}\n"
        f"⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {join_str}\n"
        f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str}",
        disable_web_page_preview=True
    )

    await client.send_message(
        user_id,
        f"👋 ʜᴇʏ {user.mention},\n"
        f"ᴛʜᴀɴᴋ ʏᴏᴜ ꜰᴏʀ ᴘᴜʀᴄʜᴀꜱɪɴɢ ᴘʀᴇᴍɪᴜᴍ.\n"
        f"ᴇɴᴊᴏʏ !! ✨🎉\n\n"
        f"⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : {amount} {unit}\n"
        f"⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {join_str}\n"
        f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str}",
        disable_web_page_preview=True
    )

    await client.send_message(
        PREMIUM_LOGS,
        f"#Added_Premium\n\n"
        f"👤 ᴜꜱᴇʀ : {user.mention}\n"
        f"⚡ ᴜꜱᴇʀ ɪᴅ : <code>{user_id}</code>\n"
        f"⏰ ᴘʀᴇᴍɪᴜᴍ ᴀᴄᴄᴇꜱꜱ : {amount} {unit}\n"
        f"⏳ ᴊᴏɪɴɪɴɢ ᴅᴀᴛᴇ : {join_str}\n"
        f"⌛️ ᴇxᴘɪʀʏ ᴅᴀᴛᴇ : {expiry_str}",
        disable_web_page_preview=True
    )


@app.on_message(filters.command("premium_users") & filters.user(SUDO_USERS))
async def premium_users_cmd(client, message: Message):
    loading = await message.reply_text("<i>ꜰᴇᴛᴄʜɪɴɢ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ...</i>")

    lines = ["⚜️ ᴘʀᴇᴍɪᴜᴍ ᴜꜱᴇʀꜱ ʟɪꜱᴛ :\n"]
    count = 1

    tz = pytz.timezone("Asia/Kolkata")
    now = datetime.datetime.now(tz)

    async for user_doc in premium_users():
        user_id = user_doc["_id"]
        expiry = user_doc.get("expire_date")

        if not expiry:
            continue

        expiry_ist = expiry.astimezone(tz)
        if expiry_ist < now:
            continue  # skip expired (optional)

        time_left = expiry_ist - now
        days = time_left.days
        hours, rem = divmod(time_left.seconds, 3600)
        minutes, _ = divmod(rem, 60)

        user = await client.get_users(user_id)
        line = (
            f"{count}. {user.mention}\n"
            f"   👤 ID: {user_id}\n"
            f"   ⏰ Left: {days}d {hours}h {minutes}m\n"
            f"   ⌛️ Expiry: {expiry_ist.strftime('%d-%m-%Y %I:%M %p')}\n"
        )
        lines.append(line)
        count += 1

    text = "".join(lines) or "No active premium users right now."

    try:
        await loading.edit_text(text)
    except MessageTooLong:
        with open("premium_users.txt", "w", encoding="utf-8") as f:
            f.write(text)
        await loading.delete()
        await message.reply_document("premium_users.txt", caption="Premium Users List")
