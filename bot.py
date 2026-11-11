import os
import telebot
from telebot import types

TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(TOKEN)

# O'yinchilar bazasi
users = {}

# Binolar narxi
BUILDINGS = {
    "uy": 50,
    "dukon": 100,
    "ferma": 200,
    "qasr": 500
}

def get_user(user_id):
    if user_id not in users:
        users[user_id] = {"gold": 0, "buildings": []}
    return users[user_id]

@bot.message_handler(commands=['start'])
def start(message):
    get_user(message.from_user.id)
    bot.reply_to(message, "Salom! Imperiya bot ishlayapti 👑\nOltin olish uchun /gold yoz\nBino qurish uchun /build yoz")

@bot.message_handler(commands=['gold'])
def gold(message):
    user = get_user(message.from_user.id)
    user["gold"] += 10
    bot.reply_to(message, f"Siz 10 ta oltin oldingiz! 💰\nHozir: {user['gold']} ta oltin")

@bot.message_handler(commands=['balance'])
def balance(message):
    user = get_user(message.from_user.id)
    bot.reply_to(message, f"💰 Oltining: {user['gold']}\n🏰 Binolaring: {len(user['buildings'])} ta")

@bot.message_handler(commands=['build'])
def build(message):
    markup = types.InlineKeyboardMarkup()
    for name, price in BUILDINGS.items():
        markup.add(types.InlineKeyboardButton(f"{name} - {price} 💰", callback_data=f"build_{name}"))
    bot.reply_to(message, "Qaysi bino qurasan? 🏰", reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("build_"))
def build_callback(call):
    name = call.data.replace("build_", "")
    price = BUILDINGS[name]
    user = get_user(call.from_user.id)
    if user["gold"] >= price:
        user["gold"] -= price
        user["buildings"].append(name)
        bot.answer_callback_query(call.id, f"{name} qurildi! 🎉")
        bot.send_message(call.message.chat.id, f"Tabriklayman! {name} qurding! 🏰\nQolgan oltin: {user['gold']} 💰")
    else:
        bot.answer_callback_query(call.id, f"Oltin yetmaydi! Kerak: {price}, Borda: {user['gold']}", show_alert=True)

@bot.message_handler(commands=['my'])
def my(message):
    user = get_user(message.from_user.id)
    if not user["buildings"]:
        bot.reply_to(message, "Hali binoying yo'q. /build bilan qur!")
    else:
        text = "Sening binolaring 🏰:\n" + "\n".join([f"- {b}" for b in user["buildings"]])
        bot.reply_to(message, text)

bot.polling(none_stop=True)
