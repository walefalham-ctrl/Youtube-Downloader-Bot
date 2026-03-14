import telebot
import yt_dlp
import os
import uuid
import logging
from dotenv import load_dotenv

load_dotenv()
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

API_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
if not API_TOKEN:
    raise RuntimeError("⚠️ ضع توكن البوت في متغير البيئة TELEGRAM_BOT_TOKEN")

bot = telebot.TeleBot(API_TOKEN, parse_mode='HTML')
os.makedirs('downloads', exist_ok=True)
MAX_SIZE = 50 * 1024 * 1024  # 50MB

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 مرحباً! أرسل رابط يوتيوب أو تيك توك وسأقوم بتحميله لك.\nاكتب /help للمزيد.")

@bot.message_handler(commands=['help'])
def help_cmd(message):
    bot.reply_to(message, "📥 أرسل رابط فيديو من يوتيوب أو تيك توك.\n⚠️ الحد: 50 ميجابايت، جودة 720p كحد أقصى.")

@bot.message_handler(func=lambda m: True)
def handle_url(message):
    url = message.text.strip()
    if not any(domain in url for domain in ['youtube.com', 'youtu.be', 'tiktok.com']):
        bot.reply_to(message, "❌ يرجى إرسال رابط صحيح من يوتيوب أو تيك توك.")
        return

    sent = bot.reply_to(message, "⏳ جاري التحميل...")
    filename = None
    
    try:
        ydl_opts = {
            'format': 'best[height<=720][ext=mp4]/best[height<=720]/best',
            'outtmpl': f'downloads/{message.chat.id}_{uuid.uuid4()}.%(ext)s',
            'geo_bypass': True,
            'geo_bypass_country': 'US',
            'noplaylist': True,
            'socket_timeout': 30,
            'retries': 3,
            'quiet': True,
            'no_warnings': True,
        }
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)
        
        if not filename or not os.path.exists(filename):
            raise FileNotFoundError("لم يتم العثور على الملف بعد التحميل")
            
        if os.path.getsize(filename) > MAX_SIZE:
            bot.edit_message_text("❌ الملف أكبر من 50 ميجابايت. البوت لا يدعم الملفات الكبيرة.", 
                                message.chat.id, sent.message_id)
            return

        caption = f"✅ <b>{info.get('title', 'تم التحميل')}</b>"
        with open(filename, 'rb') as f:
            bot.send_video(message.chat.id, f, caption=caption, timeout=600)
        
        bot.delete_message(message.chat.id, sent.message_id)
        
    except Exception as e:
        logging.exception("Error during download/send")
        bot.edit_message_text(f"❌ حدث خطأ: {str(e)[:100]}", message.chat.id, sent.message_id)
        
    finally:
        if filename and os.path.exists(filename):
            try:
                os.remove(filename)
            except:
                pass

logging.info("🤖 البوت يعمل الآن...")
bot.polling(none_stop=True, timeout=30)

