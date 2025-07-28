from pyrogram import Client, filters
from pyrogram.types import Message, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from .database import save_file, get_file_by_id
from .fs_checker import check_subscription
from .config import BOT_USERNAME

@Client.on_message(filters.private & filters.command("start"))
async def start(bot, message: Message):
    if not await check_subscription(bot, message):
        return

    if len(message.command) > 1:
        file_id = message.command[1]
        data = await get_file_by_id(file_id)
        if data:
            await message.reply_document(file_id, caption=f"📄 {data['file_name']}")
        else:
            await message.reply("⚠️ File not found.")
    else:
        buttons = InlineKeyboardMarkup([[
            InlineKeyboardButton("ℹ️ About Me", callback_data="about")
        ]])
        await message.reply("👋 Welcome! Send me a file and I’ll give you a shareable link.", reply_markup=buttons)

@Client.on_message(filters.private & filters.document & ~filters.grouped)
async def single_file(bot, message: Message):
    if not await check_subscription(bot, message):
        return

    file = message.document
    await save_file(file.file_id, file.file_name)

    link = f"https://t.me/{BOT_USERNAME}?start={file.file_id}"
    await message.reply_text(f"✅ File Saved!\n🔗 Shareable Link:\n{link}")

@Client.on_message(filters.private & filters.grouped)
async def batch_files(bot, message: Message):
    if not await check_subscription(bot, message):
        return

    links = []
    for msg in message.grouped_messages:
        if msg.document:
            await save_file(msg.document.file_id, msg.document.file_name)
            link = f"https://t.me/{BOT_USERNAME}?start={msg.document.file_id}"
            links.append(f"📄 {msg.document.file_name} → {link}")

    if links:
        await message.reply_text("✅ Batch Upload Complete:\n\n" + "\n".join(links))
    else:
        await message.reply("⚠️ No valid documents found in batch.")

@Client.on_callback_query(filters.regex("about"))
async def about_callback(bot, query: CallbackQuery):
    text = (
        "**🤖 About This Bot**\n\n"
        "This is a Telegram File Store Bot built using Pyrogram.\n"
        "📦 Upload files and get permanent shareable links.\n"
        "📢 You must join our @AJ_TVSERIAL updates channel to use this bot.\n\n"
        "🛠 Developed with ❤️ by @AJ_TVSERIAL"
    )
    await query.message.edit_text(text, disable_web_page_preview=True)
