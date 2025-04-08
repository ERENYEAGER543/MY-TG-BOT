import requests
import time
from flask import Request, jsonify
from telebot import TeleBot, types
from telebot.types import Update

# === CONFIGURATION ===
TOKEN = "YOUR_BOT_TOKEN"  # Replace manually
OWNER_ID = 6823641974
FIREBASE_URL = "https://memory-d65f1-default-rtdb.firebaseio.com"

bot = TeleBot(TOKEN)

# === Firebase Functions ===
def set_data(path, data):
    requests.put(f"{FIREBASE_URL}/{path}.json", json=data)

def get_data(path):
    res = requests.get(f"{FIREBASE_URL}/{path}.json")
    return res.json()

# === Command: /start ===
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,
        "Yo! I'm a Like Bot made by @KingPaid1\n\n"
        "Commands:\n"
        "/like <server_name> <uid>\n"
        "/allow (owner only)"
    )

# === Command: /allow ===
@bot.message_handler(commands=['allow'])
def allow(message):
    if message.from_user.id != OWNER_ID:
        bot.reply_to(message, "Only my master can use this.")
        return
    if not message.chat.type.endswith("group"):
        bot.reply_to(message, "Use this only in groups.")
        return
    set_data(f"allowed_groups/{message.chat.id}", {"allowed": True})
    bot.reply_to(message, "This group is now blessed by the bot gods!")

# === Command: /like ===
@bot.message_handler(commands=['like'])
def like(message):
    chat_id = str(message.chat.id)
    user_id = str(message.from_user.id)

    # Check if group is allowed
    group_data = get_data(f"allowed_groups/{chat_id}")
    if not group_data or not group_data.get("allowed"):
        bot.reply_to(message, "This group is not allowed. Ask the owner to use /allow.")
        return

    # Check cooldown
    cooldown = get_data(f"cooldowns/{user_id}")
    if cooldown:
        last = cooldown.get("last_used", 0)
        if time.time() - last < 86400:
            remaining = int(86400 - (time.time() - last))
            hrs = remaining // 3600
            mins = (remaining % 3600) // 60
            bot.reply_to(message, f"Chill! Try again in {hrs}h {mins}m.")
            return

    try:
        args = message.text.split()
        if len(args) != 3:
            bot.reply_to(message, "Usage: /like <server_name> <uid>")
            return

        server_name, uid = args[1], args[2]
        api_url = f"https://uditanshu-like-api.vercel.app/like?server_name={server_name}&uid={uid}"
        res = requests.get(api_url).json()

        if res.get("error") == "Failed to retrieve initial player info.":
            bot.reply_to(message, "Accounts are banned or expired. Wait for reset🌚")
        elif res.get("status") == 1:
            set_data(f"cooldowns/{user_id}", {"last_used": time.time()})
            bot.reply_to(message,
                f"✅ Likes Sent!\n\n"
                f"👤 Player: {res['PlayerNickname']}\n"
                f"🆔 UID: {res['UID']}\n"
                f"👍 Before: {res['LikesbeforeCommand']}\n"
                f"✅ Given: {res['LikesGivenByAPI']}\n"
                f"🎯 After: {res['LikesafterCommand']}"
            )
        else:
            bot.reply_to(message, "Something unexpected happened. Try again later.")
    except Exception as e:
        print("Error:", e)
        bot.reply_to(message, "Oops! Something went wrong.")

# === Webhook Handler for Vercel ===
def handler(request: Request):
    if request.method == "POST":
        json_data = request.get_json()
        update = Update.de_json(json_data)
        bot.process_new_updates([update])
        return jsonify({"ok": True})
    return "This is the bot webhook!", 200
