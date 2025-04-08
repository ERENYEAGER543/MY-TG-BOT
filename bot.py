import requests
import time
from telebot import TeleBot, types

TOKEN = "7910521495:AAGc0-hhaoiS_bC-zPO9XvEDSZvz3MtWa-E"
OWNER_ID = 6823641974

bot = TeleBot(TOKEN)
allowed_groups = set()
user_cooldowns = {}

# Send startup message when bot is started
@bot.message_handler(commands=['start'])
def send_welcome(message):
    if message.chat.type == "private":
        bot.send_message(message.chat.id,
            "Hey! This is the **Like Bot** made by @KingPaid1\n\n"
            "Use `/like <server_name> <uid>` to send likes.\n"
            "Note: You can only use it once every 24 hours if successful.\n"
            "If it fails, you can try again!\n\n"
            "if you want to this bot in your group 😉 contact @DcOwnersBot 🙏.",
            parse_mode='Markdown')

# Command for the owner to allow group usage
@bot.message_handler(commands=['allow'])
def allow_group(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "Only the bot owner can use this command.")
        return
    if message.chat.type in ["group", "supergroup"]:
        allowed_groups.add(message.chat.id)
        bot.reply_to(message, "Bot is now allowed to work in this group.")
    else:
        bot.reply_to(message, "This command can only be used in groups.")

# Like command
@bot.message_handler(commands=['like'])
def like(message):
    if message.chat.type in ["group", "supergroup"] and message.chat.id not in allowed_groups:
        bot.reply_to(message, "Bot is not allowed to work in this group. Ask the owner to use /allow.")
        return

    user_id = message.from_user.id
    now = time.time()

    # check cooldown
    if user_id in user_cooldowns and now - user_cooldowns[user_id]["timestamp"] < 86400 and user_cooldowns[user_id]["status"] == "success":
        bot.reply_to(message, "You can only use this command once every 24 hours after a successful request.")
        return

    try:
        args = message.text.split()
        if len(args) != 3:
            bot.reply_to(message, "Usage: /like <server_name> <uid>")
            return

        server_name, uid = args[1], args[2]
        api_url = f"https://king-like-api-two.vercel.app/like?server_name={server_name}&uid={uid}"
        
        response = requests.get(api_url).json()

        if "error" in response and response["error"] == "Failed to retrieve initial player info.":
            bot.reply_to(message, "Accounts are banned or token expired, wait till owners exchange🌚")
            user_cooldowns[user_id] = {"timestamp": now, "status": "fail"}
        elif "status" in response and response["status"] == 1:
            bot.reply_to(message, 
                f"✅ Likes Sent Successfully!\n\n"
                f"👤 Player: {response['PlayerNickname']}\n"
                f"🆔 UID: {response['UID']}\n"
                f"👍 Before: {response['LikesbeforeCommand']}\n"
                f"✅ Given: {response['LikesGivenByAPI']}\n"
                f"🎯 After: {response['LikesafterCommand']}"
            )
            user_cooldowns[user_id] = {"timestamp": now, "status": "success"}
        else:
            bot.reply_to(message, "An unexpected error occurred, please try again later.")
            user_cooldowns[user_id] = {"timestamp": now, "status": "fail"}
    except Exception as e:
        bot.reply_to(message, "An error occurred while processing your request.")
        print(f"Error: {e}")

bot.polling()
