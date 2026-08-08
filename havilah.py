import telebot
import os
import time

BOT_TOKEN = os.getenv("BOT_TOKEN") # We go set this on Railway

time.sleep(10)
bot = telebot.TeleBot(BOT_TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Havilah 2.0 dey online on Railway! 🔥 Send me text")

print("HAVILAH 2.0 IS ONLINE!!!")
bot.polling(none_stop=True)