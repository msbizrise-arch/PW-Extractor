import os, asyncio, importlib, logging, threading
from logging.handlers import RotatingFileHandler
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from Extractor.modules import ALL_MODULES

logging.basicConfig(level=logging.INFO, format="%(name)s - %(message)s",
                    handlers=[RotatingFileHandler("log.txt", maxBytes=5000000, backupCount=10), logging.StreamHandler()])

async def boot():
    for module in ALL_MODULES:
        importlib.import_module("Extractor.modules." + module)
    print("» PW EXTRACTOR BOT STARTED SUCCESSFULLY 🚀")
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
