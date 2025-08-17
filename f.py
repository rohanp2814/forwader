# forward_bot.py

import os
from telethon import TelegramClient, events
import asyncio
from flask import Flask
import threading
mport telethon
from dotenv import load_dotenv

# ================== LOAD .ENV ==================
load_dotenv()

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
SESSION_NAME = os.getenv("SESSION_NAME", "my_session")

# Comma-separated list of source channels in .env
SOURCE_CHANNELS = [
    int(c.strip()) if c.strip().startswith("-") or c.strip().isdigit() else c.strip()
    for c in os.getenv("SOURCE_CHANNELS", "").split(",")
    if c.strip()
]
DEST_CHANNEL = int(os.getenv("DEST_CHANNEL")) if os.getenv("DEST_CHANNEL") else None
# =================================================

app = Flask(__name__)

@app.route("/")
def home():
    return "Telegram Forwarder Bot is Running ✅"


async def run_bot():
    client = TelegramClient(f"sessions/{SESSION_NAME}", API_ID, API_HASH)
    await client.start()
    print("🚀 Bot is running... Forwarding media files automatically.")

    # Resolve source channels
    resolved_sources = []
    for chat in SOURCE_CHANNELS:
        try:
            entity = await client.get_entity(chat)
            resolved_sources.append(entity)
            print(f"✅ Resolved source channel: {chat}")
        except Exception as e:
            print(f"❌ Could not resolve {chat} -> {e}")

    # Resolve destination
    try:
        dest_entity = await client.get_entity(DEST_CHANNEL)
        print(f"✅ Resolved destination channel: {DEST_CHANNEL}")
    except Exception as e:
        print(f"❌ Could not resolve destination {DEST_CHANNEL}: {e}")
        return

    @client.on(events.NewMessage(chats=resolved_sources))
    async def handler(event):
        try:
            if event.media:
                await client.forward_messages(dest_entity, event.message)
                print(f"📩 Forwarded media from {event.chat_id} -> {DEST_CHANNEL}")
            else:
                print("⏩ Skipped non-media message.")
        except Exception as e:
            print("❌ Error forwarding:", e)

    await client.run_until_disconnected()


def start_bot_loop():
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.run_until_complete(run_bot())


if __name__ == "__main__":
    os.makedirs("sessions", exist_ok=True)  # keep sessions separate
    # Run the bot in a separate thread
    t = threading.Thread(target=start_bot_loop)
    t.start()

    # Run Flask app
    app.run(host="0.0.0.0", port=int(os.getenv("PORT", 5000)))
