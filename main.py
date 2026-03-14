import telebot
import yt_dlp
import os

# التوكن الجديد حقك
API_TOKEN = '8647831819:AAGyv_LwCIxKd9jT-ezeKmT2C6ni45TjV3c'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "أهلاً بك! أرسل لي رابط تيك توك وسأقوم بتحميله لك بدون علامة مائية فوراً.")

@bot.message_handler(func=lambda message: 'tiktok.com' in message.text)
def download_tiktok(message):
    url = message.text
    chat_id = message.chat.id
    sent_msg = bot.reply_to(message, "⏳ جاري جلب الفيديو من تيك توك...")

    ydl_opts = {
        'format': 'best',
        'outtmpl': f'tiktok_{chat_id}.%(ext)s',
        'quiet': True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        with open(filename, 'rb') as video:
            bot.send_video(chat_id, video, caption="✅ تم التحميل بنجاح!")
        
        os.remove(filename) # مسح الملف فوراً
        bot.delete_message(chat_id, sent_msg.message_id)
    except Exception as e:
        bot.edit_message_text(f"❌ خطأ: تأكد من الرابط أو حاول لاحقاً.", chat_id, sent_msg.message_id)

bot.polling(none_stop=True)
