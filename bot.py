import telebot
import requests
import os

# 🔹 Bot Token (Railway pe ENV Variable me set karna)
BOT_TOKEN = os.getenv("BOT_TOKEN")
API_URL = "https://KING-LIKE-API.vercel.app/like?uid={}&server_name=ind"

bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, "🔥 Welcome! Use /like <UID> to get likes.")

@bot.message_handler(commands=['like'])
def like(message):
    try:
        params = message.text.split()
        if len(params) < 2:
            bot.reply_to(message, "❌ Usage: /like <UID>")
            return
        
        uid = params[1]  # Extract UID
        response = requests.get(API_URL.format(uid)).json()
        
        # ✅ API Response Handling
        if response.get("status") == 1:
            bot.reply_to(
                message,
                f"✅ *Likes Sent Successfully!*\n\n"
                f"👤 *Player:* {response.get('PlayerNickname')}\n"
                f"🆔 *UID:* {response.get('UID')}\n"
                f"👍 *Likes Before:* {response.get('LikesbeforeCommand')}\n"
                f"🔥 *Likes After:* {response.get('LikesafterCommand')}\n",
                parse_mode="Markdown"
            )
        else:
            bot.reply_to(message, "❌ Failed to send likes. Try again!")

    except Exception as e:
        bot.reply_to(message, f"❌ Error: {str(e)}")

# 🔥 Bot Start
bot.polling()
