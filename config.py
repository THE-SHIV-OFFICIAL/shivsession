"""Bot configuration. Keep Telegram credentials in environment variables only."""
from os import getenv
from dotenv import load_dotenv

load_dotenv()


def required(name):
    value = getenv(name, "").strip()
    if not value:
        raise ValueError(f"Set {name} in your environment before starting the bot")
    return value


API_ID = int(required("API_ID"))
API_HASH = required("API_HASH")
BOT_TOKEN = required("BOT_TOKEN")
MONGO_DB_URI = required("MONGO_DB_URI")
OWNER_ID = int(required("OWNER_ID"))
LOG_GROUP_ID = int(getenv("LOG_GROUP_ID", "0"))
SUDO_USERS = [int(x) for x in getenv("SUDO_USERS", "").replace(",", " ").split()]
MUST_JOIN = [x.strip().lstrip("@") for x in getenv("MUST_JOIN", "BETABOT_HUB BETABOT_SUPPORT SUKOON_S").replace(",", " ").split() if x.strip()]
START_IMG_URL = [x.strip() for x in getenv("START_IMG", "https://files.catbox.moe/gyeoqw.jpg").split(",") if x.strip()]
SUPPORT_CHAT = getenv("SUPPORT_CHAT", "betabot_support").lstrip("@")
UPDATE_CHANNEL = getenv("UPDATE_CHANNEL", "betabot_hub").lstrip("@")
