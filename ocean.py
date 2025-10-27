import os
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = "8453006624:AAEyrJYa75NqM-NXeXB_I8GQ7DHnC4chvM8"  # langsung assign token di sini (hati-hati)

def ambil_chart_selenium(symbol: str) -> str:
    symbol = symbol.upper()
    url = f"https://www.tradingview.com/chart/?symbol=IDX:{symbol}"
    filename = f"{symbol}.png"

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # mode tanpa GUI
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--window-size=1920,1080")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    driver = webdriver.Chrome(options=chrome_options)
    try:
        driver.get(url)
        time.sleep(12)  # tunggu chart load, bisa disesuaikan
        driver.save_screenshot(filename)
    finally:
        driver.quit()

    return filename

async def chart(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if not context.args:
        await update.message.reply_text("Gunakan format: /chart <kode_saham>\nContoh: /chart BBCA")
        return

    symbol = context.args[0].upper()
    await update.message.reply_text(f"Mengambil chart untuk {symbol}...")

    try:
        filename = ambil_chart_selenium(symbol)
        with open(filename, "rb") as f:
            await update.message.reply_photo(photo=f)
        os.remove(filename)
    except Exception as e:
        await update.message.reply_text(f"Gagal mengambil chart: {e}")

def main():
    app = ApplicationBuilder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("chart", chart))
    app.run_polling()

if __name__ == "__main__":
    main()
