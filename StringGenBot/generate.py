"""Generate Pyrogram or Telethon string sessions in a private conversation."""
import random
import re

from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton
from pyrogram.errors import SessionPasswordNeeded as PyroPasswordNeeded
from telethon import TelegramClient
from telethon.sessions import StringSession
from telethon.errors import SessionPasswordNeededError as TelePasswordNeeded

from config import API_ID, API_HASH, START_IMG_URL
from StringGenBot.must_join import require_membership
from StringGenBot.premium_emoji import premium

ask_ques = f"{premium('star')} **Choose the session type to generate**\n\nPowered by BETA BOT HUB"
buttons_ques = [
    [InlineKeyboardButton("Pyrogram", callback_data="pyrogram"), InlineKeyboardButton("Telethon", callback_data="telethon")],
    [InlineKeyboardButton("Pyrogram bot", callback_data="pyrogram_bot"), InlineKeyboardButton("Telethon bot", callback_data="telethon_bot")],
    [InlineKeyboardButton("⬅️ Back", callback_data="start_menu")],
]
gen_button = [[InlineKeyboardButton("Generate session", callback_data="generate")]]


@Client.on_message(filters.private & filters.command(["generate", "gen", "string", "str"]))
async def main(bot: Client, msg: Message):
    await msg.reply_photo(
        photo=random.choice(START_IMG_URL), caption=ask_ques,
        reply_markup=InlineKeyboardMarkup(buttons_ques),
    )


async def ask_input(bot, user_id, prompt, timeout=300):
    try:
        answer = await bot.ask(user_id, prompt + "\n\n/cancel to stop.", filters=filters.text, timeout=timeout)
    except TimeoutError:
        await bot.send_message(user_id, "Time limit reached. Tap Generate to try again.", reply_markup=InlineKeyboardMarkup(gen_button))
        return None
    if answer.text.strip().startswith("/") and answer.text.strip() != "/skip":
        await answer.reply_text("Session generation cancelled.", reply_markup=InlineKeyboardMarkup(gen_button))
        return None
    return answer


async def generate_session(bot: Client, msg: Message, telethon=False, old_pyro=False, is_bot=False, user_id=None):
    # A callback message belongs to the bot, not the person who pressed it.
    user_id = user_id or msg.chat.id
    if not await require_membership(bot, user_id, msg):
        return
    kind = ("Telethon" if telethon else "Pyrogram") + (" bot" if is_bot else "")
    await msg.reply_text(f"{premium('star')} Generating your {kind} session.")
    api_answer = await ask_input(bot, user_id, "Send your API_ID (or /skip to use this bot's API settings).")
    if api_answer is None:
        return
    if api_answer.text.strip() == "/skip":
        api_id, api_hash = API_ID, API_HASH
    else:
        try:
            api_id = int(api_answer.text.strip())
            if api_id <= 0:
                raise ValueError
        except ValueError:
            await api_answer.reply_text("API_ID must be a positive number. Please start again.")
            return
        hash_answer = await ask_input(bot, user_id, "Send your API_HASH.")
        if hash_answer is None:
            return
        api_hash = hash_answer.text.strip()
        if not re.fullmatch(r"[a-fA-F0-9]{32}", api_hash):
            await hash_answer.reply_text("API_HASH must be 32 hexadecimal characters. Please start again.")
            return
        await hash_answer.delete()
    account_answer = await ask_input(bot, user_id, "Send the BotFather bot token." if is_bot else "Send your Telegram phone number with country code, e.g. +9195XXXXXXXX.")
    if account_answer is None:
        return
    account = account_answer.text.strip()
    if is_bot and not re.fullmatch(r"\d+:[A-Za-z0-9_-]{20,}", account):
        await account_answer.reply_text("Invalid bot token format. Please start again.")
        return
    if not is_bot and not re.fullmatch(r"\+\d{7,15}", account.replace(" ", "")):
        await account_answer.reply_text("Invalid phone number. Include the country code and try again.")
        return
    if not is_bot:
        account = account.replace(" ", "")
    if is_bot:
        await account_answer.delete()
    client = TelegramClient(StringSession(), api_id, api_hash) if telethon else Client(
        "generated", api_id=api_id, api_hash=api_hash, in_memory=True,
    )
    connected = False
    try:
        await client.connect()
        connected = True
        if is_bot:
            if telethon:
                await client.sign_in(bot_token=account)
            else:
                await client.sign_in_bot(account)
        else:
            if telethon:
                code = await client.send_code_request(account)
            else:
                code = await client.send_code(account)
            otp_answer = await ask_input(bot, user_id, "Send the Telegram login code (digits only).", timeout=600)
            if otp_answer is None:
                return
            otp = otp_answer.text.replace(" ", "")
            if not otp.isdigit():
                await otp_answer.reply_text("Login code must contain digits only. Please start again.")
                return
            await otp_answer.delete()
            try:
                if telethon:
                    await client.sign_in(phone=account, code=otp, phone_code_hash=code.phone_code_hash)
                else:
                    await client.sign_in(account, code.phone_code_hash, otp)
            except (PyroPasswordNeeded, TelePasswordNeeded):
                password_answer = await ask_input(bot, user_id, "Send your two-step verification password.")
                if password_answer is None:
                    return
                password = password_answer.text
                await password_answer.delete()
                if telethon:
                    await client.sign_in(password=password)
                else:
                    await client.check_password(password=password)
        session = client.session.save() if telethon else await client.export_session_string()
        result = f"{premium('check')} **Your {kind} string session**\n\n`{session}`\n\nKeep this private. Anyone with this string can access the account."
        if is_bot:
            await bot.send_message(user_id, result)
        else:
            # Telethon uses a different markup parser; send a plain text fallback.
            saved = f"Your {kind} string session\n\n{session}\n\nKeep this private. Anyone with this string can access the account."
            await client.send_message("me", saved if telethon else result)
    except Exception:
        # Never send the underlying exception to chat: libraries can include
        # phone numbers, credentials or session details in their error text.
        await bot.send_message(user_id, f"{premium('warning')} Could not generate the session. Check your API settings and login details, then try again.", reply_markup=InlineKeyboardMarkup(gen_button))
    else:
        destination = "this chat" if is_bot else "your Saved Messages"
        await bot.send_message(user_id, f"{premium('check')} Your {kind} string session is in {destination}.")
    finally:
        if connected:
            await client.disconnect()
