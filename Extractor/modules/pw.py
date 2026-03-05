import requests
import asyncio
import os
import math
from Extractor import app
from pyrogram import filters

# ====================== OTP + TOKEN FUNCTIONS ======================
async def get_otp(message, phone_no):
    url = "https://api.penpencil.co/v1/users/get-otp"
    data = {"phone": phone_no, "countryCode": "+91"}
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, json=data, headers=headers)
        if resp.status_code == 200:
            await message.reply_text("✅ OTP sent to your number. Send OTP now.")
            return True
        else:
            await message.reply_text("❌ Failed to send OTP. Try again.")
            return False
    except:
        await message.reply_text("❌ Network error in OTP.")
        return False

async def get_token(message, phone_no, otp):
    url = "https://api.penpencil.co/v3/oauth/token"
    data = {
        "username": f"+91{phone_no}",
        "otp": otp,
        "client_id": "5eb393ee95fab7468a79d189",
        "client_secret": "KjPXuAVfC5xbmgreETNMaL7z",
        "grant_type": "password"
    }
    headers = {"Content-Type": "application/json"}
    try:
        resp = requests.post(url, json=data, headers=headers).json()
        if "access_token" in resp:
            token = resp["access_token"]
            await message.reply_text("✅ Login successful!")
            await pw_login(message, token)
            return token
        else:
            await message.reply_text("❌ Wrong OTP. Try again.")
            return None
    except:
        await message.reply_text("❌ Token error.")
        return None

async def pw_mobile(app, message):
    await message.reply_text("📱 Send your mobile number (without +91)")
    phone_msg = await app.ask(message.chat.id, "Example: 9876543210")
    phone = phone_msg.text.strip()
    
    if await get_otp(message, phone):
        otp_msg = await app.ask(message.chat.id, "🔢 Send the OTP you received")
        otp = otp_msg.text.strip()
        await get_token(message, phone, otp)

async def pw_token(app, message):
    await message.reply_text("🔑 Send your PW Token")
    token_msg = await app.ask(message.chat.id, "Paste token here")
    token = token_msg.text.strip()
    await pw_login(message, token)

# ====================== FULL VIDEO + NOTES EXTRACTION ======================
async def pw_login(message, token):
    headers = {
        "Host": "api.penpencil.co",
        "authorization": f"Bearer {token}",
        "client-id": "5eb393ee95fab7468a79d189",
        "client-version": "12.84",
        "user-agent": "Android",
        "randomid": "e4307177362e86f1",
        "client-type": "MOBILE",
        "content-type": "application/json",
    }

    # Batches
    resp = requests.get("https://api.penpencil.co/v3/batches/my-batches", headers=headers).json()
    aa = "**Your Batches:**\n\n"
    for d in resp.get("data", []):
        aa += f"**{d['name']}** : `{d['_id']}`\n"
    await message.reply_text(aa)

    batch_msg = await app.ask(message.chat.id, "**Send Batch ID**")
    batch_id = batch_msg.text.strip()
    batch_name = next((d['name'] for d in resp.get("data", []) if d['_id'] == batch_id), batch_id)

    # Subjects
    details = requests.get(f"https://api.penpencil.co/v3/batches/{batch_id}/details", headers=headers).json()
    subjects = details.get("data", {}).get("subjects", [])
    bb = "**Subjects:**\n\n"
    vj = ""
    for s in subjects:
        bb += f"**{s['subject']}** : `{s['subjectId']}`\n"
        vj += f"{s['subjectId']}&"
    await message.reply_text(bb)

    sub_msg = await app.ask(message.chat.id, f"Send Subject IDs (e.g. `1&2&3` or `{vj}`)")
    subject_ids = [x.strip() for x in sub_msg.text.split("&") if x.strip()]

    filename = f"{batch_name}_PW_Videos.txt"
    with open(filename, "w") as f:
        f.write(f"Physics Wallah - {batch_name}\n\n")

    await message.reply_text("🚀 Starting full extraction...")

    for sid in subject_ids:
        await message.reply_text(f"📚 Processing Subject: {sid}")
        
        # Videos with pagination
        page = 1
        while True:
            params = {"page": str(page), "contentType": "videos"}
            r = requests.get(f"https://api.penpencil.co/v3/batches/{batch_id}/subject/{sid}/contents", params=params, headers=headers).json()
            data = r.get("data", [])
            if not data: break
            for item in data:
                if item.get("url"):
                    title = item.get("topic", "Unknown")
                    url = item["url"].replace("d1d34p8vz63oiq", "d26g5bnklkwsh4").replace("mpd", "m3u8").strip()
                    with open(filename, "a") as f:
                        f.write(f"{title}:{url}\n")
            page += 1
            await asyncio.sleep(1)

    await app.send_document(message.chat.id, filename, caption="✅ Extraction Complete!\nDirect M3U8 links ready!")
    if os.path.exists(filename):
        os.remove(filename)
