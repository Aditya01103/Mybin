import logging
from openai import OpenAI
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Konfigurasi Token & Client
TELEGRAM_BOT_TOKEN = "8965822074:AAE6S3JeT-QaOE3YI6Mv5DcFEiTLTnZJLNs"

client = OpenAI(
    base_url="https://router.bynara.id/v1",
    api_key="sk-nry-OJUR8q42AbxuU_nQU19zcNCA43TNAqM87109jwv5i9I",
)

# Logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

# Fungsi kirim pesan ke AI Bynara
def ask_ai(user_text: str) -> str:
    try:
        res = client.chat.completions.create(
            model="agnes-2.5-flash",
            messages=[{"role": "user", "content": user_text}],
        )
        return res.choices[0].message.content
    except Exception as e:
        return f"Terjadi kesalahan koneksi: {str(e)}"

# Handler perintah /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Halo! Aku bot AI Agnes. Tulis pesan apa aja, nanti aku jawab!")

# Handler untuk balas pesan teks
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_input = update.message.text
    
    # Kirim indikator typing
    await context.bot.send_chat_action(chat_id=update.effective_chat.id, action="typing")
    
    # Ambil & kirim balasan AI
    ai_response = ask_ai(user_input)
    await update.message.reply_text(ai_response)

if __name__ == '__main__':
    app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    print("Bot Telegram berjalan...")
    app.run_polling()
