import telebot
import yt_dlp
import os

# التوكن الخاص بك
API_TOKEN = '8647831819:AAGyv_LwCIxKd9jT-ezeKmT2C6ni45TjV3c'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "مرحباً محمد! أرسل رابط تيك توك أو يوتيوب (حتى المحجوب) وسأقوم بتحميله لك.")

@bot.message_handler(func=lambda message: True)
def handle_message(message):
    url = message.text
    chat_id = message.chat.id
    
    if 'youtube.com' in url or 'youtu.be' in url or 'tiktok.com' in url:
        sent_msg = bot.reply_to(message, "⏳ جاري المعالجة وتخطي الحظر الجغرافي... انتظر قليلاً.")
        
        ydl_opts = {
            # اختيار أفضل جودة لا تزيد عن 720p لضمان سرعة الرفع وتجنب انهيار السيرفر
            'format': 'best[height<=720][ext=mp4]/best',
            'outtmpl': f'media_{chat_id}.%(ext)s',
            'geo_bypass': True, # هذه الميزة لتخطي حظر المسلسلات في السعودية
            'nocheckcertificate': True,
            'quiet': True
        }

        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                filename = ydl.prepare_filename(info)
                
            with open(filename, 'rb') as media:
                bot.send_video(chat_id, media, caption="✅ تم التحميل بنجاح!")
            
            os.remove(filename)
            bot.delete_message(chat_id, sent_msg.message_id)
        except Exception as e:
            bot.edit_message_text(f"❌ حدث خطأ: قد يكون الفيديو طويل جداً أو محمي بشكل صارم.", chat_id, sent_msg.message_id)
    else:
        bot.reply_to(message, "يرجى إرسال رابط صحيح من يوتيوب أو تيك توك.")

bot.polling(none_stop=True)
