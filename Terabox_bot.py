import os
import requests
from telegram import Bot
from telegram.ext import Updater, MessageHandler, Filters
import re

# Aapka Telegram Bot Token
TOKEN = "7117804326:AAHuHZBPAR9jewxx7j84hTzb9Q426-Ss4wE"

# Folder jisme videos ko store karega
if not os.path.exists("downloads"):
    os.makedirs("downloads")

def download_video(url):
    # File ko server pe store karega
    filename = f"downloads/video_{len(os.listdir('downloads')) + 1}.mp4"
    
    # Video download kar raha hai
    response = requests.get(url, stream=True)
    with open(filename, 'wb') as file:
        for chunk in response.iter_content(chunk_size=1024*1024):
            if chunk:
                file.write(chunk)
    
    return filename

def handle_message(update, context):
    text = update.message.text
    
    # Check agar link TeraBox ka hai
    if "terabox" in text:
        update.message.reply_text("📥 Downloading your video... Please wait.")
        
        # Extract the video link from text
        video_url = re.findall(r'(https?://[^\s]+)', text)[0]
        
        # Video ko download karein
        video_file = download_video(video_url)
        
        # Video ko Telegram pe bhej do
        with open(video_file, 'rb') as video:
            update.message.reply_video(video)
        
        # File ko delete NHI karega jab tak aap na chaho
        update.message.reply_text(f"✅ Video sent successfully!\n\n🎬 File saved on server: {video_file}")
    else:
        update.message.reply_text("❌ Please send a valid TeraBox link.")

def main():
    bot = Bot(token=TOKEN)
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    # Handle incoming messages
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))
    
    # Start the bot
    updater.start_polling()
    updater.idle()

if __name__ == "__main__":
    main()
