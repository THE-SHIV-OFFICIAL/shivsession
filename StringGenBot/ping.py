import time
import random # ✅ Added random module
from datetime import datetime
from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

# ✅ Changed START_IMG to START_IMG_URL
from config import START_IMG_URL, SUPPORT_CHAT
from StringGenBot.premium_emoji import premium

BOT_START_TIME = time.time()


def get_readable_time(seconds: int) -> str:
    count = 0
    up_time = ""
    time_list = []
    time_suffix_list = ["s", "m", "h", "d"]

    while count < 4 and seconds > 0:
        count += 1
        if count < 3:
            remainder, result = divmod(int(seconds), 60)
        else:
            remainder, result = divmod(int(seconds), 24)
        if result != 0:
            time_list.append(f"{result}{time_suffix_list[count - 1]}")
        seconds = remainder

    return ":".join(reversed(time_list))


@Client.on_message(filters.command("ping") & filters.private)
async def ping_handler(client: Client, message: Message):
    start = time.time()
    temp = await message.reply(f"**{premium('sparkle')} ᴘɪɴɢɪɴɢ... ᴡᴀɪᴛ ʙᴀʙʏ**")
    end = time.time()
    latency = (end - start) * 1000
    uptime = get_readable_time(time.time() - BOT_START_TIME)

    await temp.delete()

    # ✅ Random image fetch logic added here
    if isinstance(START_IMG_URL, list):
        start_img = random.choice(START_IMG_URL)
    else:
        start_img = START_IMG_URL

    await message.reply_photo(
        photo=start_img, # ✅ Updated to use the random image
        caption=f"""**⊚ ʜᴇʏ ʙᴀʙʏ !!

˹ sᴛʀɪɴɢ ˣ ɢᴇɴᴇʀᴀᴛᴏʀ ˼ ɪꜱ ᴀʟɪᴠᴇ 🥀 ᴀɴᴅ ᴡᴏʀᴋɪɴɢ ғɪɴᴇ

➥ ᴘᴏɴɢ: `{latency:.3f} ms`
➥ {premium('clock')} ᴜᴘᴛɪᴍᴇ: {uptime}

⦿ ᴄʀᴇᴀᴛᴇᴅ ʙʏ [THE sʜɪᴠ](https://t.me/SUKOON_S)**

{premium('heart')} 𝐏ᴏᴡєʀєᴅ 𝐁ʏ ➛ BETA BOT HUB.🙂❤️""",
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("💌 sᴜᴘᴘᴏʀᴛ", url=f"https://t.me/{SUPPORT_CHAT}"),
                    InlineKeyboardButton("🗑️ ᴄʟᴏsᴇ", callback_data="close_ping")
                ]
            ]
        )
    )


@Client.on_callback_query(filters.regex("close_ping"))
async def close_ping_cb(_, query: CallbackQuery):
    try:
        await query.message.delete()
    except:
        await query.answer("ᴄᴀɴ'ᴛ ʙᴇ ᴅᴇʟᴇᴛᴇᴅ", show_alert=True)
