[14:15, 08/08/2026] apostleword96: print("Havilah AGENT is running...")
bot.infinity_polling()
[14:17, 08/08/2026] apostleword96: import telebot
import os
import random
from groq import Groq
BOT_TOKEN=os.getenv("BOT_TOKEN")
GROQ_KEY=os.getenv("GROQ_API_KEY")
bot=telebot.TeleBot(BOT_TOKEN)
client=Groq(api_key=GROQ_KEY)
bible_verses=["For I know the plans I have for you - Jeremiah 29:11","The Lord is my shepherd - Psalm 23:1","I can do all things through Christ - Philippians 4:13","Be strong and courageous - Joshua 1:9","Trust in the Lord - Proverbs 3:5"]
def get_bible_verse():
 return f"📖 {random.choice(bible_verses)}"
def chat_with_ai(user_message):
 response=client.chat.completions.create(model="llama-3.1-8b-instant",messages=[{"role":"system","content":"You are Havilah, a helpful and business-minded AI assistant."},{"role":"user","content":user_message}])
 return response.choices[0].message.content
@bot.message_handler(func=lambda message:True)
def handle_message(message):
 text=message.text.lower()
 if "verse" in text or "bible" in text:
  bot.reply_to(message,get_bible_verse())
 else:
  ai_response=chat_with_ai(message.text)
  bot.reply_to(message,ai_response)
print("Havilah running")
bot.infinity_polling()
