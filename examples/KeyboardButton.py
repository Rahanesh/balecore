from BotCore import MainBot, ReplyKeyboardMarkup, KeyboardButton
import asyncio

bot = MainBot(
    Token="YOUR TOKEN", 
    url="https://tapi.bale.ai"
)

@bot.Message(bot.filters.command("start") & bot.filters.private())
async def send_reply_keyboard(bot: MainBot, update, full_update, message, User=None, File=None):
    keyboard = ReplyKeyboardMarkup(
        [KeyboardButton("گزینه ۱"), KeyboardButton("گزینه ۲")],
        resize_keyboard=True,
        one_time_keyboard=True
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text="یک گزینه انتخاب کنید:",
        reply_markup=keyboard.to_dict()
    )

@bot.Message(bot.filters.text() & bot.filters.private())
async def handle_keyboard_selection(bot: MainBot, update, full_update, message, User=None, File=None):
    user_message = message.text
    if user_message == "گزینه ۱":
        await bot.send_message(
            chat_id=message.chat.id,
            text="شما گزینه ۱ را انتخاب کردید."
        )
    elif user_message == "گزینه ۲":
        await bot.send_message(
            chat_id=message.chat.id,
            text="شما گزینه ۲ را انتخاب کردید."
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