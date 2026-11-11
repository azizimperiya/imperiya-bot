import os
import telebot

TOKEN = os.environ.get("BOT_TOKEN", “9198086333:AAHupvEMLz3FaHHJ9zhL3cIQkv8FSIt2LeA")

bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start'])
def start(m):
    bot.send_message(m.chat.id, "Salom! Imperiya bot ishlayapti 👑\nOltin olish uchun /gold yoz")

@bot.message_handler(commands=['gold'])
def gold(m):
    bot.send_message(m.chat.id, "Siz 10 ta oltin oldingiz! 🪙")

@bot.message_handler(func=lambda m: True)
def echo(m):
    bot.send_message(m.chat.id, "Yozdingiz: " + m.text)

print("Bot ishga tushdi...")
bot.polling(none_stop=True)
