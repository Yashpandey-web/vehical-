import os
import logging
import requests
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

BOT_TOKEN = os.getenv("8443953787:AAGCU5cHTlaB5GC60SLJqcZpAgiNK4Q80Sw")   # Token from BotFather
API_URL = os.getenv("https://revangevichelinfo.vercel.app/api/rc?number=")       # Example: https://yourapi.com/vehicle?number=

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(_name_)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("🚗 Send me a vehicle number to search.")

async def handle_vehicle(update: Update, context: ContextTypes.DEFAULT_TYPE):
    vehicle_number = update.message.text.strip().upper()
    await update.message.reply_text(f"🔎 Searching for {vehicle_number}...")

    try:
        response = requests.get(API_URL + vehicle_number)
        if response.status_code == 200:
            data = response.json()
            result = f"""
🚘 Vehicle Info
━━━━━━━━━━━━━━━
RC: {data.get('rc_number')}
Owner: {data.get('owner_name')}
Father: {data.get('father_name')}
Model: {data.get('maker_model')}
Fuel: {data.get('fuel_type')}
Reg Date: {data.get('registration_date')}
Insurance Expiry: {data.get('insurance_expiry')}
RTO: {data.get('rto')}
Address: {data.get('address')}
━━━━━━━━━━━━━━━
"""
            await update.message.reply_text(result, parse_mode="Markdown")
        else:
            await update.message.reply_text("❌ Vehicle not found or API error.")
    except Exception as e:
        await update.message.reply_text(f"⚠ Error: {e}")

def main():
    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_vehicle))
    print("✅ Bot is running...")
    app.run_polling()

if _name_ == "_main_":
    main()