import os

API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
MONGO_URI = os.environ.get("MONGO_URI")
FSUB_CHANNEL = int(os.environ.get("FSUB_CHANNEL"))  # Channel ID with -100
BOT_USERNAME = os.environ.get("BOT_USERNAME")  # Without @
