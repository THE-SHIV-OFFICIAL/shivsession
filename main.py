import config
import time
import logging
import asyncio # ✅ Added asyncio import

# ✅ --- ASYNCIO EVENT LOOP FIX FOR PYTHON 3.12+ ---
try:
    loop = asyncio.get_event_loop()
except RuntimeError:
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
# --------------------------------------------------

from pyrogram import Client, idle
from pyromod import listen  
from pyrogram.errors import ApiIdInvalid, ApiIdPublishedFlood, AccessTokenInvalid

# Configure logging
logging.basicConfig(
    level=logging.INFO, 
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

logging.getLogger("pymongo").setLevel(logging.ERROR)

# Initialize start time
StartTime = time.time()

# Initialize the Client
app = Client(
    "Anonymous",
    api_id=config.API_ID,
    api_hash=config.API_HASH,
    bot_token=config.BOT_TOKEN,
    in_memory=True,
    plugins=dict(root="StringGenBot"),
)

if __name__ == "__main__":
    print("𝚂𝚝𝚛𝚊𝚗𝚐𝚎𝚛 𝚂𝚎𝚜𝚜𝚒𝚘𝚗 𝙶𝚎𝚗 𝚜𝚝𝚊𝚛𝚝𝚒𝚗𝚐...")
    try:
        app.start()
    except ApiIdInvalid:
        raise Exception("Your API_ID is not valid.")
    except ApiIdPublishedFlood:
        raise Exception("Your API_ID/API_HASH is flood banned.")
    except AccessTokenInvalid:
        raise Exception("Your BOT_TOKEN is not valid.")
    except Exception as e:
        logging.error(f"An unexpected error occurred: {e}")
        raise

    me = app.get_me()
    uname = me.username
    print(f"@{uname} NOW STRANGER SESSION GEN IS READY TO GEN SESSION")
    
    # --- LOG GROUP MESSAGE (STARTUP LOG) ---
    LOG_GROUP_ID = getattr(config, "LOG_GROUP_ID", None)
    
    if LOG_GROUP_ID:
        try:
            app.send_message(
                LOG_GROUP_ID,
                f"**🤖 ʙᴏᴛ sᴛᴀʀᴛᴇᴅ sᴜᴄᴄᴇssғᴜʟʟʏ!**\n\n**✨ ʙᴏᴛ:** @{uname}\n**👤 ᴏᴡɴᴇʀ ɪᴅ:** `{config.OWNER_ID}`\n**🤞 ᴘᴏᴡᴇʀᴇᴅ ʙʏ ➛ BETA BOT HUB.🙂❤️**"
            )
            logging.info("Startup log sent to Log Group successfully.")
        except Exception as e:
            logging.error(f"Log Group Message Failed! Make sure the bot is an Admin in the Log Group. Error: {e}")
    # ----------------------------------------
    
    idle()
    
    app.stop()
    print("🇸 🇪 🇸 🇸 🇮 🇴 🇳  🇬 🇪 🇳 🇷 🇦 🇹 🇮 🇳 🇬  🇸 🇹 🇴 🇵 🇵 🇪 🇩...")
