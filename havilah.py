import telebot
import os
import random
from groq import Groq

# 1. GET SECRETS FROM RAILWAY
BOT_TOKEN = os.getenv("BOT_TOKEN")
GROQ_KEY = os.getenv("GROQ_API_KEY")

# 2. START BOT + AI
bot = telebot.TeleBot(BOT_TOKEN)
client = Groq(api_key=GROQ_KEY)

# 3. BIBLE VERSES - ONLY WHEN REQUESTED
bible_verses = [
    "For I know the plans I have for you - Jeremiah 29:11",
    "The Lord is my shepherd, I shall not want - Psalm 23:1",
    "I can do all things through Christ who strengthens me - Philippians 4:13",
    "Be strong and courageous. Do not be afraid - Joshua 1:9",
    "Trust in the Lord with all your heart - Proverbs 3:5"
]

def get_bible_verse():
    return f"📖 {random.choice(bible_verses)}"

# 4. TALK TO GROQ AI
def chat_with_ai(user_message):
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "You are Havilah, a versatile, helpful, and business-minded AI assistant. Be direct, smart, and valuable."},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content

# 5. WHEN SOMEONE MESSAGES THE BOT
@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.lower()
    
    # Check if user asked for a verse
    if "verse" in text or "bible" in text or "scripture" in text:
        bot.reply_to(message, get_bible_verse())
    else:
        # Normal AI chat
        ai_response = chat_with_ai(message.text)
        bot.reply_to(message, ai_response)

print("Havilah AGENT is running...")
bot.infinity_polling()
