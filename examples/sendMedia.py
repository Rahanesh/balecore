from BaleCore import MainBot
import asyncio

bot = MainBot(
    Token="YOUR_BOT_TOKEN", 
    url="https://tapi.bale.ai"
)

@bot.Message(bot.filters.command("file") & bot.filters.private())
async def send_file(bot: MainBot, update, full_update, message, User=None, File=None):
    await bot.send_document(
        chat_id=message.chat.id,
        document="path/to/your/file.pdf"
    )

@bot.Message(bot.filters.command("photo") & bot.filters.private())
async def send_photo(bot: MainBot, update, full_update, message, User=None, File=None):
    await bot.send_photo(
        chat_id=message.chat.id,
        photo="path/to/your/photo.jpg"
    )

@bot.Message(bot.filters.command("voice") & bot.filters.private())
async def send_voice(bot: MainBot, update, full_update, message, User=None, File=None):
    await bot.send_voice(
        chat_id=message.chat.id,
        voice="path/to/your/voice.ogg"
    )

@bot.Message(bot.filters.command("music") & bot.filters.private())
async def send_music(bot: MainBot, update, full_update, message, User=None, File=None):
    await bot.send_audio(
        chat_id=message.chat.id,
        audio="path/to/your/music.mp3"
    )

async def run_bot():
    await asyncio.gather(
        bot.start()
    )

if __name__ == "__main__":
    try:
        asyncio.run(run_bot())
    except KeyboardInterrupt:
        print("Shutting down the bot...")
        asyncio.run(bot.stop())