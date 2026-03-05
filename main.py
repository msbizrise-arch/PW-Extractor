import os
import logging
from flask import Flask, request, jsonify
import asyncio
import nest_asyncio
nest_asyncio.apply()

from pyrogram import Client
from Extractor import app as pyrogram_app  # Global client
from Extractor.modules import ALL_MODULES
import importlib

logging.basicConfig(level=logging.INFO, format="%(name)s - %(message)s")
LOGGER = logging.getLogger(__name__)

flask_app = Flask(__name__)

# Load modules (handlers on global client)
for module in ALL_MODULES:
    importlib.import_module(f"Extractor.modules.{module}")

@flask_app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "PW-Extractor Online"})

@flask_app.route("/webhook", methods=["POST"])
async def webhook():
    update = request.get_json()
    await pyrogram_app.handle_update(update)  # Process with global client
    return jsonify({"ok": True})

if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    # Start client & set webhook
    webhook_url = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME', 'pw-extractor-omks')}.onrender.com/webhook"
    loop.run_until_complete(pyrogram_app.start())
    loop.run_until_complete(pyrogram_app.set_webhook(url=webhook_url))
    LOGGER.info(f"Bot started & webhook set to {webhook_url}")
    
    # Run Flask (gunicorn/Procfile handles in prod)
    port = int(os.getenv("PORT", 10000))
    flask_app.run(host="0.0.0.0", port=port, debug=False)
