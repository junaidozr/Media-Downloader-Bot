import os
import yt_dlp
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

# Koyeb-ൽ കൊടുക്കുന്ന Token ഇവിടെ സ്വയം എടുക്കും
TOKEN = os.environ.get("BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("ഹലോ! ഏതെങ്കിലും വീഡിയോ ലിങ്ക് അയക്കൂ (YouTube, Insta Reels, FB etc.), ഞാൻ ഡൗൺലോഡ് ചെയ്തു തരാം.")

async def download_video(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    if not url or not url.startswith("http"):
        return

    msg = await update.message.reply_text("Please wait.... Downloaing....😉")

    ydl_opts = {
        'format': 'best[ext=mp4]/best',
        'outtmpl': 'downloads/%(id)s.%(ext)s',
        'max_filesize': 45 * 1024 * 1024,  # സൗജന്യ ബോട്ടിന് 45MB വരെ
        'quiet': True
    }

    try:
        # വീഡിയോ ഡൗൺലോഡ് ചെയ്യുന്നു
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            filename = ydl.prepare_filename(info)

        await msg.edit_text("ടെലഗ്രാമിലേക്ക് അപ്‌ലോഡ് ചെയ്യുന്നു... 📤")
        
        # തിരികെ ടെലഗ്രാമിലേക്ക് അയക്കുന്നു
        with open(filename, 'rb') as video_file:
            await update.message.reply_video(video=video_file)

        # മെമ്മറി ലാഭിക്കാൻ വീഡിയോ സെർവറിൽ നിന്ന് നീക്കം ചെയ്യുന്നു
        if os.path.exists(filename):
            os.remove(filename)
            
        await msg.delete()

    except Exception as e:
        await msg.edit_text(f"ക്ഷമിക്കണം, ഡൗൺലോഡ് ചെയ്യാൻ പറ്റിയില്ല (45MB-ൽ താഴെയുള്ള ലിങ്കുകൾ ഉപയോഗിക്കുക).\nError: {str(e)[:100]}")

def main():
    if not TOKEN:
        print("BOT_TOKEN ലഭ്യമല്ല!")
        return

    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, download_video))
    
    print("Bot is running...")
    app.run_polling()

if __name__ == '__main__':
    main()
  
