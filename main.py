import telebot
import yt_dlp
import os
from flask import Flask
from threading import Thread

# --- إعدادات البوت ---
API_TOKEN = '8647831819:AAFo8_JxQXN5uMAdIlN458ja1bsL_G15q94'
bot = telebot.TeleBot(API_TOKEN)

# --- إعداد سيرفر وهمي لإرضاء Render ---
app = Flask('')

@app.route('/')
def home():
    return "البوت شغال 24/7"

def run_web():
    # Render يعطينا المنفذ تلقائياً في متغير اسمه PORT
    port = int(os.environ.get("PORT", 5000))
    app.run(host='0.0.0.0', port=port)

# --- أوامر البوت ---
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أرسل رابط يوتيوب وسأقوم بتحميله بأعلى جودة.")

@bot.message_handler(func=lambda message: 'youtube.com' in message.text or 'youtu.be' in message.text)
def download_video(message):
    try:
        url = message.text
        bot.reply_to(message, "⏳ جاري التحميل بأعلى جودة..")
        ydl_opts = {'format': 'best', 'outtmpl': 'video.%(ext)s'}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        with open(filename, 'rb') as video:
            bot.send_video(message.chat.id, video)
        os.remove(filename)
    except Exception as e:
        bot.reply_to(message, f"❌ خطأ: {e}")

# --- تشغيل البوت والسيرفر معاً ---
if __name__ == "__main__":
    # تشغيل السيرفر الوهمي في خلفية الكود
    t = Thread(target=run_web)
    t.start()
    print("🚀 البوت انطلق في السحاب...")
    bot.polling(none_stop=True)
