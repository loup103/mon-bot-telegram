import asyncio
import requests
import google.generativeai as genai
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Configurations Telegram
TELEGRAM_TOKEN = "8818308490:AAFMFvrUjt0qb5ObwIMqaYwtFfheQHjvHi8"
CHAT_ID = "7136655238"
BANKROLL_TOTALE = 1000

# Clé API IA Gemini
GEMINI_API_KEY = "AQ.Ab8RN6Jf0uAeWytVsdLkMtp2Okc290Ta_cZALyjerOgN5_5GUw"

# Configuration du modèle IA
genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel("gemini-1.5-flash")

# Calcul de la mise conseillée
def calculer_mise(chute_pct, bankroll):
    if chute_pct >= 15.0:
        pct = 0.03
    elif chute_pct >= 10.0:
        pct = 0.02
    else:
        pct = 0.01
    return round(bankroll * pct, 2), (pct * 100)

# Discussion avec l'IA Telegram
async def repondre_discussion(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question_utilisateur = update.message.text
    print(f"Question reçue : {question_utilisateur}")
    
    try:
        response = model.generate_content(question_utilisateur)
        await update.message.reply_text(response.text)
    except Exception as e:
        await update.message.reply_text("Désolé, une erreur est survenue lors de la réponse.")
        print(f"Erreur IA : {e}")

# Commande /start
async def commande_start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = (
        "🤖 **Bonjour ! Je suis votre assistant IA et bot de paris.**\n\n"
        "• Posez-moi n'importe quelle question directement ici, je vous répondrai !\n"
        "• Je continue de surveiller les cotes et anomalies en arrière-plan."
    )
    await update.message.reply_text(msg, parse_mode="Markdown")

# Surveillance automatique en arrière-plan
async def boucle_surveillance(app):
    while True:
        print("[⚽] Surveillance des cotes en cours...")
        await asyncio.sleep(900)

async def main():
    app = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    app.add_handler(CommandHandler("start", commande_start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, repondre_discussion))

    async with app:
        await app.start()
        await app.updater.start_polling()
        print("🤖 Bot Telegram et IA prêts à discuter !")
        await boucle_surveillance(app)
        await app.updater.stop()
        await app.stop()

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    asyncio.run(main())
