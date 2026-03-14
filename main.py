import telebot
import yt_dlp
import os

# التوكن الخاص بك
API_TOKEN = '8647831819:AAGyv_LwCIxKd9jT-ezeKmT2C6ni45TjV3c'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً بك! أنا شغال الآن من السحاب 24/7. أرسل رابط يوتيوب.")

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
        bot.reply_to(message, f"❌ حدث خطأ: {e}")

if __name__ == "__main__":
    print("🚀 البوت انطلق بنجاح كـ Background Worker...")
    bot.polling(none_stop=True)
