"""Selected IDs from the provided Premium Emoji list.

Pyrogram 2 accepts <emoji id="..."> tags in text/captions. Keyboard buttons
only accept plain Unicode emojis on this version, so keep those as-is.
"""

EMOJI_IDS = {
    "star": ("🌟", "5195174505458200077"),
    "heart": ("❤️", "6266992763930158001"),
    "check": ("✅", "5215492745900077682"),
    "warning": ("⚠️", "5215305227627931680"),
    "back": ("⬅️", "5215361191051798408"),
    "letter": ("✉️", "6264777724741556322"),
    "sparkle": ("✨", "5350444080084033572"),
    "clock": ("⏰", "6285240160120477644"),
    "chart": ("📊", "6100593065024562684"),
}


def premium(name):
    character, emoji_id = EMOJI_IDS[name]
    return f'<emoji id="{emoji_id}">{character}</emoji>'
