from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, CallbackQueryHandler, ContextTypes, MessageHandler, filters

# ---------- BOT XABARLARI ----------
START_MESSAGE = "Salom! Men F1 TOGETHER kanalining rasmiy botiman 😊 🏎"
HELP_MESSAGE = (
    "Mavjud komandalar:\n"
    "/start - Botni ishga tushirish\n"
    "/help - Yordam\n"
    "/info - Bot haqida ma'lumot\n"
    "/admin - Admin bilan bog‘lanish\n"
    "/menu - Tugmalar menyusi"
)
INFO_MESSAGE = "Men F1 TOGETHER kanalining rasmiy botiman! 🚀"
ADMIN_MESSAGE = "Admin bilan bog‘lanish: @olimjonov103"

# ---------- INLINE TUGMALAR MENYUSI ----------
def get_inline_keyboard():
    
    keyboard = [
        [InlineKeyboardButton("ℹ️ Info", callback_data="info"),
         InlineKeyboardButton("🆘 Help", callback_data="help")],
        [InlineKeyboardButton("👤 Admin", callback_data="admin"),
         InlineKeyboardButton("🏎 F1 News", callback_data="f1_news")],
        [InlineKeyboardButton("🔙 Ortga", callback_data="back")]  # yangi ortga tugma
    ]
    return InlineKeyboardMarkup(keyboard)

# ---------- /start komandasi ----------
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        START_MESSAGE,
        reply_markup=get_inline_keyboard()
    )

# ---------- /help komandasi ----------
async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(HELP_MESSAGE)

# ---------- /info komandasi ----------
async def info_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(INFO_MESSAGE)

# ---------- /admin komandasi ----------
async def admin_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(ADMIN_MESSAGE)

# ---------- /menu komandasi ----------
async def menu_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Menyudan tanlang:",
        reply_markup=get_inline_keyboard()
    )

# ---------- CALLBACK QABUL QILISH (INLINE TUGMALAR) ----------
async def button_callback(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()  # tugma bosilganda loading tugmasini olib tashlaydi

    if query.data == "info":
        await query.edit_message_text(INFO_MESSAGE, reply_markup=get_inline_keyboard())
    elif query.data == "help":
        await query.edit_message_text(HELP_MESSAGE, reply_markup=get_inline_keyboard())
    elif query.data == "admin":
        await query.edit_message_text(ADMIN_MESSAGE, reply_markup=get_inline_keyboard())
    elif query.data == "f1_news":
        photo_url = "https://www.topgear.com/sites/default/files/images/news-article/2022/09/e707701e270bf1f4c63247dd6dcf32ce/220041-scuderia-ferrari-dutch-gp-sunday.jpg?w=1280&h=720"
        await query.edit_message_text("F1 News rasmi quyida:", reply_markup=get_inline_keyboard())
        await context.bot.send_photo(chat_id=query.message.chat_id, photo=photo_url)
    elif query.data == "back":
        await query.edit_message_text("Bosh menyuga qaytdingiz:", reply_markup=get_inline_keyboard())

# ---------- AUTO-REPLY FUNKSIYASI ----------
async def auto_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.lower()
    if "salom" in text:
        await update.message.reply_text("Salom! 🏎")
    elif "yangilik" in text or "news" in text:
        await update.message.reply_text("F1 yangiliklari uchun /menu tugmasini bosing.")
    elif "admin" in text:
        await update.message.reply_text("Admin bilan bog‘lanish: @olimjonov103")
    else:
        await update.message.reply_text("Kechirasiz, men buni tushunmadim. /help tugmasini bosing.")

# ---------- BOT ISHLASH QISMI ----------
app = ApplicationBuilder().token("").build()

# Komandalar
app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("menu", menu_command))
app.add_handler(CommandHandler("help", help_command))
app.add_handler(CommandHandler("info", info_command))
app.add_handler(CommandHandler("admin", admin_command))

# Inline tugmalar
app.add_handler(CallbackQueryHandler(button_callback))

# Auto-reply
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, auto_reply))

# Botni ishga tushurish
print("F1 TOGETHER Premium bot ishga tushdi! Telegram’da /start yozib sinab ko‘ring.")
app.run_polling()
