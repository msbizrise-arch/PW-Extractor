import os
import threading
import logging
from flask import Flask, jsonify
from pyrogram import Client, idle
from config import API_ID, API_HASH, BOT_TOKEN
from Extractor.modules import ALL_MODULES
import importlib

# Logging setup
logging.basicConfig(
    level=logging.INFO,
    format="%(name)s - %(message)s",
    handlers=[logging.StreamHandler()]
)
LOGGER = logging.getLogger(__name__)

# Flask app for Render healthcheck
flask_app = Flask(__name__)

@flask_app.route("/", methods=["GET"])
def health_check():
    return jsonify({"status": "PW-Extractor Online and Running"})

# Load all modules (handlers register automatically)
for module in ALL_MODULES:
    importlib.import_module(f"Extractor.modules.{module}")

# Bot startup function (run in background thread)
def start_bot():
    client = Client(
        "PWExtractor",
        api_id=API_ID,
        api_hash=API_HASH,
        bot_token=BOT_TOKEN
    )
    
    client.start()
    LOGGER.info("» PW EXTRACTOR BOT STARTED SUCCESSFULLY 🚀")
    idle()  # Keeps the bot polling forever
    client.stop()

if __name__ == "__main__":
    # Start bot polling in a background thread
    bot_thread = threading.Thread(target=start_bot, daemon=True)
    bot_thread.start()
    
    # Run Flask server (Render requires this for web service)
    port = int(os.getenv("PORT", 10000))  # Render uses $PORT, default fallback
    flask_app.run(host="0.0.0.0", port=port, debug=False)
