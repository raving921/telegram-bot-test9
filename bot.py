import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Application, CommandHandler, CallbackQueryHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.environ.get('BOT_TOKEN')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        [InlineKeyboardButton("🎮 Oyun Oyna", callback_data='oyun')],
        [InlineKeyboardButton("📚 Yardım", callback_data='yardim')],
        [InlineKeyboardButton("ℹ️ Hakkında", callback_data='hakkinda')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text(
        f"👋 Merhaba {update.effective_user.first_name}!\n\n"
        "Ben basit bir test botuyum.\n"
        "Aşağıdaki butonları kullanabilirsin:",
        reply_markup=reply_markup
    )

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    
    if query.data == 'oyun':
        keyboard = [
            [InlineKeyboardButton("🎲 Zar At", callback_data='zar')],
            [InlineKeyboardButton("🎯 Dart At", callback_data='dart')],
            [InlineKeyboardButton("🔙 Geri", callback_data='geri')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("🎮 Oyun seç:", reply_markup=reply_markup)
    
    elif query.data == 'zar':
        await query.message.reply_dice(emoji='🎲')
        await query.message.reply_text("🎲 Zar atıldı!")
    
    elif query.data == 'dart':
        await query.message.reply_dice(emoji='🎯')
        await query.message.reply_text("🎯 Dart atıldı!")
    
    elif query.data == 'yardim':
        await query.edit_message_text(
            "📚 **Yardım Menüsü**\n\n"
            "Komutlar:\n"
            "/start - Botu başlat\n"
            "/merhaba - Selamlaşma\n"
            "/bilgi - Bot hakkında bilgi",
            parse_mode='Markdown'
        )
    
    elif query.data == 'hakkinda':
        await query.edit_message_text(
            "ℹ️ **Bot Hakkında**\n\n"
            "📌 Versiyon: 1.0\n"
            "👨‍💻 Python Telegram Bot",
            parse_mode='Markdown'
        )
    
    elif query.data == 'geri':
        keyboard = [
            [InlineKeyboardButton("🎮 Oyun Oyna", callback_data='oyun')],
            [InlineKeyboardButton("📚 Yardım", callback_data='yardim')],
            [InlineKeyboardButton("ℹ️ Hakkında", callback_data='hakkinda')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await query.edit_message_text("Ana menüye döndün!", reply_markup=reply_markup)

async def merhaba(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"👋 Merhaba {update.effective_user.first_name}!")

async def bilgi(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🤖 Ben bir Telegram botuyum!")

async def mesaj_cevapla(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if 'merhaba' in update.message.text.lower():
        await update.message.reply_text("👋 Merhaba!")
    else:
        await update.message.reply_text(f"Yazdın: {update.message.text}")

def main():
    if not BOT_TOKEN:
        print("❌ BOT_TOKEN bulunamadı!")
        return
    
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("merhaba", merhaba))
    app.add_handler(CommandHandler("bilgi", bilgi))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, mesaj_cevapla))
    
    print("✅ Bot çalışıyor!")
    app.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()
