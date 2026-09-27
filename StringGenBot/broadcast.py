import asyncio
from pyrogram import Client, filters
from pyrogram.errors import FloodWait, UserIsBlocked, InputUserDeactivated

# Sahi import path database se users laane ke liye
from StringGenBot.db.users import get_served_users
from config import OWNER_ID
from StringGenBot.premium_emoji import premium

# Safe import SUDO_USERS ke liye
try:
    from config import SUDO_USERS
except ImportError:
    SUDO_USERS = []

ALLOWED_USERS = [OWNER_ID] + (SUDO_USERS if isinstance(SUDO_USERS, list) else [])

@Client.on_message(filters.command("broadcast") & filters.user(ALLOWED_USERS))
async def broadcast_msg(client, message):
    if not message.reply_to_message:
        return await message.reply_text("⚠️ Bhai, us message par reply karo jise broadcast karna hai!")

    b_msg = await message.reply_text("⏳ **Broadcast shuru ho raha hai...**\nKripya wait karein.")
    
    users = await get_served_users()
    total_users = len(users)
    successful = 0
    failed = 0

    for user in users:
        user_id = user["user_id"] # DB se ID fetch ki
        
        try:
            await message.reply_to_message.copy(chat_id=user_id)
            successful += 1
            await asyncio.sleep(0.1) # API limits se bachne ke liye chota delay
            
        except FloodWait as e:
            await asyncio.sleep(e.value)
            await message.reply_to_message.copy(chat_id=user_id)
            successful += 1
            
        except (UserIsBlocked, InputUserDeactivated):
            # User ne block kar diya hai ya account delete ho gaya hai
            failed += 1
            
        except Exception:
            # Koi unknown error aaye toh usko bhi skip karega
            failed += 1

    # Final report message update karna
    await b_msg.edit_text(
        f"{premium('check')} **Broadcast Pura Hua!**\n\n"
        f"{premium('chart')} **Total Users:** `{total_users}`\n"
        f"{premium('check')} **Bheja Gaya:** `{successful}`\n"
        f"❌ **Fail Hua:** `{failed}`"
    )
