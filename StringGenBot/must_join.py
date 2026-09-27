"""One join-check shared by messages and session callbacks."""
from config import MUST_JOIN
from pyrogram import Client, filters
from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from StringGenBot.premium_emoji import premium


async def require_membership(bot, user_id, message):
    missing = []
    for channel in MUST_JOIN:
        try:
            await bot.get_chat_member(channel, user_id)
        except UserNotParticipant:
            missing.append(channel)
        except Exception:
            # A missing admin permission or inaccessible channel must not
            # be mistaken for a user who has not joined.
            raise RuntimeError(f"Cannot verify @{channel}; add the bot as an admin there")
    if not missing:
        return True
    buttons = [[InlineKeyboardButton(f"Join @{channel}", url=f"https://t.me/{channel}")] for channel in missing]
    buttons.append([InlineKeyboardButton("✅ Check again", callback_data="check_join")])
    await message.reply_text(
        f"{premium('warning')} Please join the channels below, then tap Check again.",
        reply_markup=InlineKeyboardMarkup(buttons),
    )
    return False


@Client.on_message(filters.incoming & filters.private & filters.command(["start", "gen", "generate", "str", "string"]), group=-1)
async def must_join_channel(bot: Client, msg: Message):
    try:
        joined = await require_membership(bot, msg.from_user.id, msg)
    except RuntimeError:
        await msg.reply_text("Membership check is temporarily unavailable. Please contact support.")
        joined = False
    if not joined:
        msg.stop_propagation()


@Client.on_callback_query(filters.regex(r"^check_join$"))
async def check_join(bot, query):
    try:
        joined = await require_membership(bot, query.from_user.id, query.message)
    except RuntimeError:
        await query.answer("Membership check unavailable. Contact support.", show_alert=True)
        return
    if joined:
        await query.answer("Verified! Tap Generate string to continue.", show_alert=True)
    else:
        await query.answer()
