import telebot
import yt_dlp
import os

# التوكن الخاص بك
API_TOKEN = '8647831819:AAFo8_JxQXN5uMAdIlN458ja1bsL_G15q94'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً بك! أرسل رابط يوتيوب وسأقوم بتحميله بأعلى جودة ممكنة.")

@bot.message_handler(func=lambda message: 'youtube.com' in message.text or 'youtu.be' in message.text)
def download_video(message):
    url = message.text
    chat_id = message.chat.id
    
    bot.reply_to(message, "⏳ جاري معالجة الفيديو بجودة عالية.. قد يستغرق الأمر دقيقة.")

    # إعدادات التحميل لأعلى جودة مدمجة (فيديو + صوت)
    ydl_opts = {
        'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
        'outtmpl': 'video_%(id)s.%(ext)s',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        with open(filename, 'rb') as video:
            bot.send_video(chat_id, video, caption="✅ تم التحميل بنجاح!")
        
        # حذف الملف من السيرفر بعد الإرسال لتوفير المساحة
        os.remove(filename)
    except Exception as e:
        bot.reply_to(message, f"❌ حدث خطأ: {e}")

print("🚀 البوت شغال...")
bot.polling(none_stop=True)

# أضف هذا السطر قبل الأخير لفتح منفذ وهمي يرضي Render
import os
PORT = int(os.environ.get('PORT', 5000))

print("🚀 البوت شغال...")
# تشغيل البوت
bot.polling(none_stop=True)
