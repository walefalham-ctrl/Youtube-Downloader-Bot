import telebot
import yt_dlp
import os

API_TOKEN = '8647831819:AAGyv_LwCIxKd9jT-ezeKmT2C6ni45TjV3c'
bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(func=lambda message: 'youtube.com' in message.text or 'youtu.be' in message.text)
def download_video(message):
    url = message.text
    chat_id = message.chat.id
    sent_msg = bot.reply_to(message, "⏳ الفيديو طويل.. جاري المعالجة والرفع، قد يستغرق ذلك دقائق...")

    ydl_opts = {
        # يختار جودة متوسطة (720p أو أقل) لضمان أن الحجم لا يتعدى سعة السيرفر
        'format': 'best[height<=720][ext=mp4]/bestvideo[height<=720]+bestaudio/best',
        'outtmpl': f'video_{chat_id}.%(ext)s',
        'max_filesize': 450 * 1024 * 1024, # حد أقصى 450 ميجا لكي لا ينهار السيرفر المجاني
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
            
        with open(filename, 'rb') as video:
            bot.send_video(chat_id, video, caption="✅ تم تحميل الفيديو الطويل بنجاح!")
        
        os.remove(filename)
    except Exception as e:
        bot.edit_message_text(f"❌ تعذر تحميل هذا الملف الضخم: {str(e)[:100]}", chat_id, sent_msg.message_id)
        if os.path.exists(filename): os.remove(filename)

bot.polling(none_stop=True)
