import os
import asyncio
import threading
import importlib
import logging
from logging.handlers import RotatingFileHandler

# 🔥 PRO FIX - Render + Python 3.12/3.14 event loop crash khatam
import nest_asyncio
nest_asyncio.apply()          # ← Yeh line sabse pehle

from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from Extractor.modules import ALL_MODULES

logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(message)s",
    handlers=[
        RotatingFileHandler("log.txt", maxBytes=5000000, backupCount=10),
        logging.StreamHandler()
    ]
)

LOGGER = logging.getLogger(__name__)

async def boot():
    for module in ALL_MODULES:
        importlib.import_module("Extractor.modules." + module)
    LOGGER.info("» PW EXTRACTOR BOT STARTED SUCCESSFULLY 🚀")
    await idle()

def run_web():
    from fastapi import FastAPI
    import uvicorn
    app = FastAPI()
    @app.get("/")
    async def home(): return {"status": "PW-Extractor Online"}
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)))

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    asyncio.run(boot())
