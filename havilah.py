import telebot
import os

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = telebot.TeleBot(BOT_TOKEN)

 @bot.message_handler(commands=['start'])
 def send_welcome(message):
     bot.reply_to(message, "Hello! Havilah is online 🔥 How can I help you?")

 @bot.message_handler(func=lambda message: True)
 def echo_all(message):
     bot.reply_to(message, f"You said: {message.text}")

 print("Bot is running...")
 bot.infinity_polling()
