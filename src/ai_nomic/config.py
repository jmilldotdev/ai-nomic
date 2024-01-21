from dotenv import load_dotenv
import os

load_dotenv()

EDEN_API_KEY = os.getenv("EDEN_API_KEY")
EDEN_API_SECRET = os.getenv("EDEN_API_SECRET")
EDEN_CHARACTER_ID = os.getenv("EDEN_CHARACTER_ID")
EDEN_API_URL = os.getenv("EDEN_API_URL") or "https://api.eden.art"
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
DISCORD_WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
ALLOWED_GUILDS = [int(g) for g in os.getenv("ALLOWED_GUILDS", "").split(",")]
ALLOWED_CHANNELS = [int(c) for c in os.getenv("ALLOWED_CHANNELS", "").split(",")]
