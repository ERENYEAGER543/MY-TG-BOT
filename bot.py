import logging
import requests
from aiogram import Bot, Dispatcher, types
from aiogram.utils import executor

BOT_TOKEN = "7910521495:AAGc0-hhaoiS_bC-zPO9XvEDSZvz3MtWa-E"
OWNER_ID = 6823641974  # Tumhara Telegram ID
ALLOWED_GROUP = -1002400853476  # Sirf is group me chalega

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

logging.basicConfig(level=logging.INFO)

@dp.message_handler(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply("THE OWNER IS @KingPaid1\nCHANNEL @freeapilinks bot working channel @FFLIKEGROUP 🌚😎❤️")

@dp.message_handler(lambda msg: msg.text.startswith("/like"))
async def like_command(message: types.Message):
    user_id = message.chat.id

    if user_id != ALLOWED_GROUP and user_id != OWNER_ID:
        return await message.reply("❌ You are not allowed to use this bot in this chat.")

    try:
        command_parts = message.text.split()
        if len(command_parts) < 2:
            return await message.reply("❌ Please provide a UID. Example: `/like 12345678`")

        uid = command_parts[1]
        api_url = f"https://king-like-api.vercel.app/like?uid={uid}&server_name=IND"
        response = requests.get(api_url).json()

        if "error" in response:
            return await message.reply("🚫 GUEST ACCOUNTS BANNED OR TOKENS EXPIRED WAIT TILL OWNER ADDING.....🌚 NEW ACCOUNT")

        reply_text = (
            f"✅ Likes Given: {response['LikesGivenByAPI']}\n"
            f"👍 Likes Before: {response['LikesbeforeCommand']}\n"
            f"🔥 Likes After: {response['LikesafterCommand']}\n"
            f"🎮 Player: {response['PlayerNickname']}\n"
            f"🆔 UID: {response['UID']}"
        )
        await message.reply(reply_text)

    except Exception as e:
        await message.reply(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)
