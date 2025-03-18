from BaleCore import MainBot, InlineKeyboardMarkup, InlineKeyboardButton
import asyncio

bot = MainBot(
    Token="YOUR_BOT_TOKEN", 
    url="https://tapi.bale.ai"
)

@bot.Message(bot.filters.command("reply") & bot.filters.private())
async def reply_message(bot: MainBot, update, full_update, message, User=None, File=None):
    await bot.reply_message_auto(
        update=update,
        text="این یک پیام ریپلای است."
    )

@bot.Message(bot.filters.command("buttons") & bot.filters.private())
async def send_buttons(bot: MainBot, update, full_update, message, User=None, File=None):
    keyboard = InlineKeyboardMarkup(
        [InlineKeyboardButton("دکمه ۱", callback_data="button1")],
        [InlineKeyboardButton("دکمه ۲", callback_data="button2")]
    )
    await bot.send_message(
        chat_id=message.chat.id,
        text="یک دکمه انتخاب کنید:",
        reply_markup=keyboard
    )

@bot.CallbackQuery(bot.filters.callback_query_data_startswith("button"))
async def handle_button_click(bot: MainBot, update):
    callback_data = update.callback_query.data
    if callback_data == "button1":
        await bot.answer_callback_query(
            callback_query_id=update.callback_query.id,
            text="شما دکمه ۱ را زدید!"
        )
    elif callback_data == "button2":
        await bot.answer_callback_query(
            callback_query_id=update.callback_query.id,
            text="شما دکمه ۲ را زدید!"
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