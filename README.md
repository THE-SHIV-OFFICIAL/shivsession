# BETA BOT HUB — String Session Bot

Telegram bot for generating Pyrogram and Telethon user/bot string sessions in private chat.

## Setup

1. Install Python 3.10+ and run `pip install -r requirements.txt`.
2. Copy `sample.env` to `.env` and set `API_ID` and `API_HASH` from [my.telegram.org/apps](https://my.telegram.org/apps), `BOT_TOKEN` from [@BotFather](https://t.me/BotFather), your numeric `OWNER_ID`, and `MONGO_DB_URI`. Never commit `.env` or publish API hashes/tokens.
3. Optionally set `MUST_JOIN` to space-separated public channel usernames. Add the bot as an admin to each channel so membership checks work; set it empty to disable checks. `LOG_GROUP_ID=0` disables start logs.
4. Run `python main.py` (or use the provided Procfile/Dockerfile).

In the bot, `/start` opens the menu. Select Pyrogram or Telethon and user or bot session; `/skip` uses the configured bot API ID/hash, or provide your own pair. User sessions are sent to the user's Saved Messages; bot sessions are sent to their private bot conversation. Treat string sessions as passwords and revoke any leaked sessions via Telegram's active sessions settings.

Premium emoji IDs from the supplied list are used in messages/captions. Keyboard button labels remain normal emoji because Pyrogram 2 does not support premium emoji icons there. Some Telegram clients may show the regular emoji fallback. The bot does **not** automatically join channels using generated user sessions.

**Note:** Credentials present in earlier copies of this repository should be rotated at my.telegram.org before deploying.
