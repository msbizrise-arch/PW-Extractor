import os
import asyncio
import threading
import importlib
import logging
from logging.handlers import RotatingFileHandler

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
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8080)), loop="asyncio")

if __name__ == "__main__":
    threading.Thread(target=run_web, daemon=True).start()
    
    # Clean event loop for Render + Python 3.12
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(boot())
