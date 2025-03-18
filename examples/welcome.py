from BaleCore import MainBot
import asyncio

bot = MainBot(
    Token="YOUR_BOT_TOKEN", 
    url="https://tapi.bale.ai"
)

@bot.Message(bot.filters.command("start") & bot.filters.private())
async def welcome_message(bot: MainBot, update, full_update, message, User=None, File=None):
    await bot.send_message(
        chat_id=message.chat.id,
        text="خوش آمدید! به ربات خوش‌آمدگو خوش آمدید."
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