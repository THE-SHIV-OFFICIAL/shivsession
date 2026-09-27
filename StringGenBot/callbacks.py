from pyrogram import Client, filters
from pyrogram.types import CallbackQuery, InlineKeyboardMarkup
from StringGenBot.generate import generate_session, ask_ques, buttons_ques
from StringGenBot.premium_emoji import premium

@Client.on_callback_query(filters.regex(pattern=r"^(generate|pyrogram|pyrogram_bot|telethon_bot|telethon)$"))
async def _callbacks(bot: Client, callback_query: CallbackQuery):
    query = callback_query.matches[0].group(1)
    try:
        if query == "generate":
            await callback_query.answer()
            await callback_query.message.reply(ask_ques, reply_markup=InlineKeyboardMarkup(buttons_ques))
        elif query == "pyrogram":
            await callback_query.answer()
            await generate_session(bot, callback_query.message, user_id=callback_query.from_user.id)
        elif query == "pyrogram_bot":
            await callback_query.answer("» ᴛʜᴇ sᴇssɪᴏɴ ɢᴇɴᴇʀᴀᴛᴇᴅ ᴡɪʟʟ ʙᴇ ᴏғ ᴩʏʀᴏɢʀᴀᴍ ᴠ2.", show_alert=True)
            await generate_session(bot, callback_query.message, is_bot=True, user_id=callback_query.from_user.id)
        elif query == "telethon_bot":
            await callback_query.answer()
            await generate_session(bot, callback_query.message, telethon=True, is_bot=True, user_id=callback_query.from_user.id)
        elif query == "telethon":
            await callback_query.answer()
            await generate_session(bot, callback_query.message, telethon=True, user_id=callback_query.from_user.id)
    except Exception:
        await callback_query.message.reply(f"{premium('warning')} Something went wrong. Check your details and try again; contact support if it continues.")
