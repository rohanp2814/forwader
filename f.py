# forward_bot.py

import os
import logging
import asyncio
from telethon import TelegramClient, events
from flask import Flask

# ---------------- Logging ----------------
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("forwarder")

# ---------------- Flask ----------------
app = Flask(__name__)

@app.route("/")
def home():
    return "✅ Telegram Forwarder Bot is running!"

# ---------------- Env Variables ----------------
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_NAME = os.environ.get("SESSION_NAME", "my_session")

# Source channels: split env variable by comma into list
SOURCE_CHANNELS = os.environ.get("SOURCE_CHANNELS", "").split(",")
DEST_CHANNEL = os.environ.get("DEST_CHANNEL")

# ---------------- Telegram Client ----------------
client = TelegramClient(SESSION_NAME, API_ID, API_HASH)

@client.on(events.NewMessage(chats=SOURCE_CHANNELS))
async def handler(event):
    try:
        if event.message.media:  # forward only media files
            await client.forward_messages(DEST_CHANNEL, event.message)
            logger.info(f"Forwarded media from {event.chat_id} to {DEST_CHANNEL}")
    except Exception as e:
        logger.error(f"Error forwarding message: {e}")

# ---------------- Main ----------------
async def main():
    await client.start()
    logger.info("🚀 Forwarder Bot Started")
    await client.run_until_disconnected()

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
