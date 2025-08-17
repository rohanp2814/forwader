from pyrogram import Client, filters
from threading import Thread
from flask import Flask

API_ID = 26611044
API_HASH = "9ef2ceed3bd6ac525020d757980f6864"
SESSION_NAME = "my_session"

# Replace these with your own channel IDs or usernames as strings
SOURCE_CHANNELS = ["-1002845156656"]
DEST_CHANNEL = "-1002793017891"

app = Client(SESSION_NAME, api_id=API_ID, api_hash=API_HASH)
flask_app = Flask(__name__)

@flask_app.route("/")
def home():
    return "Bot is alive!"

@app.on_message(filters.chat(SOURCE_CHANNELS))
async def forward_to_channel(client, message):
    await message.forward(DEST_CHANNEL)

def run_flask():
    flask_app.run(host="0.0.0.0", port=8080)

if __name__ == "__main__":
    # Run Flask in a separate thread
    Thread(target=run_flask).start()
    # Run Pyrogram client
    app.run()
