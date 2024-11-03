import os
import requests
from bs4 import BeautifulSoup
from telegram import Update, Bot
from telegram.ext import CommandHandler, Updater, CallbackContext

# Retrieve token from environment variable
TOKEN = os.getenv('YOUR_TELEGRAM_BOT_TOKEN')

def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! Send /download <URL> to download a song from Flow.com.mm")

def download_song(update: Update, context: CallbackContext):
    # Get URL from user input
    url = context.args[0]
    response = requests.get(url)

    # Check response
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        # Assuming there's an FLAC link
        flac_link = soup.find('a', href=True, text='.flac')
        
        if flac_link:
            flac_url = flac_link['href']
            flac_response = requests.get(flac_url)
            if flac_response.status_code == 200:
                with open("song.flac", "wb") as f:
                    f.write(flac_response.content)
                update.message.reply_text("Download complete! Sending song...")
                context.bot.send_document(chat_id=update.effective_chat.id, document=open("song.flac", "rb"))
            else:
                update.message.reply_text("Couldn't download the FLAC file.")
        else:
            update.message.reply_text("FLAC link not found on the page.")
    else:
        update.message.reply_text("Failed to retrieve content from Flow.com.mm.")

def main():
    updater = Updater(TOKEN, use_context=True)
    dp = updater.dispatcher
    
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("download", download_song))
    
    updater.start_polling()
    updater.idle()

if __name__ == '__main__':
    main()