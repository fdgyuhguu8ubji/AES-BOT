from pyrogram.errors import UserNotParticipant
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from .config import FSUB_CHANNEL

async def check_subscription(bot, message):
    try:
        user = await bot.get_chat_member(FSUB_CHANNEL, message.from_user.id)
        if user.status not in ("member", "administrator", "creator"):
            raise UserNotParticipant()
        return True
    except UserNotParticipant:
        join_btn = InlineKeyboardMarkup(
            [[
                InlineKeyboardButton("📢 Join Channel", url=f"https://t.me/c/{str(FSUB_CHANNEL)[4:]}"),
                InlineKeyboardButton("✅ I Joined", callback_data="checksub")
            ]]
        )
        await message.reply("Please join the channel to use this bot.", reply_markup=join_btn)
        return False
