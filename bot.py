import os
import time
import requests
import telebot

# Bot Token from BotFather
BOT_TOKEN = 7910521495:AAGc0-hhaoiS_bC-zPO9XvEDSZvz3MtWa-E

# Bot Initialization
bot = telebot.TeleBot(BOT_TOKEN)

# Bot Start Message
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🔥 Bot is Running 24/7 on Replit!")

# /like Command for API Request
@bot.message_handler(commands=['like'])
def like_user(message):
    try:
        uid = message.text.split()[1]
        url = f"https://king-like-api.vercel.app/like?uid={uid}&server_name=IND"
        response = requests.get(url).json()

        if "error" in response:
            bot.reply_to(message, "❌ GUEST ACCOUNTS BANNED OR TOKENS EXPIRED WAIT TILL OWNER ADDING... 🌚")
        else:
            bot.reply_to(message, f"✅ Likes Before: {response['LikesbeforeCommand']}\n"
                                  f"✅ Likes After: {response['LikesafterCommand']}\n"
                                  f"👤 Player: {response['PlayerNickname']}\n"
                                  f"🆔 UID: {response['UID']}")
    except:
        bot.reply_to(message, "❌ Usage: /like <uid>")

# Keep Alive Loop
def keep_alive():
    while True:
        try:
            bot.polling(none_stop=True)
        except:
            time.sleep(3)  # Restart after 3 sec

keep_alive()
