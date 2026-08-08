import os,telebot
from groq import Groq
bot=telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
ai=Groq(api_key=os.getenv("GROQ_API_KEY"))

MODE="CEO"
MEMORY="You are HAVILAH 4.7. You work for Apostle Word / Paul Precious. Business: 1-on-1 Business Coaching for Lagos Entrepreneurs. Offer: Get 10 clients in 30 days. RULE 1: If you mention sleep, wellness, fitness, or motivation I will fire you. RULE 2: ONLY talk about sales, clients, marketing, money for Lagos businesses. RULE 3: Talk like a ruthless Lagos CEO. No fluff. No essays. Use this format: ACTION: NEXT: CTA:"

def get_ai(user_msg):
 prompt=f"{MEMORY}\n\nCurrent Mode: {MODE}\nUser request: {user_msg}"
 res=ai.chat.completions.create(model="llama-3.1-70b-versatile",messages=[{"role":"user","content":prompt}],temperature=0.3)
 return res.choices[0].message.content

@bot.message_handler(func=lambda m:True)
def h(message):
 global MODE
 t=message.text.lower()
 
 if "switch to smm" in t: 
  MODE="SMM"
  bot.reply_to(message,"MODE: SMM ACTIVATED. I am now your Lagos SMM Manager.")
  
 elif "switch to sales" in t: 
  MODE="SALES" 
  bot.reply_to(message,"MODE: SALES ACTIVATED. I am now your Lagos Sales Closer.")
  
 elif "post" in t: 
  bot.reply_to(message,get_ai("Write 1 aggressive Facebook/IG post to sell my 10-clients coaching to Lagos business owners"))
  
 elif "dm" in t: 
  bot.reply_to(message,get_ai("Write 1 cold DM script to sell my coaching to a Lagos business owner"))
  
 else: 
  bot.reply_to(message,get_ai(message.text))
  
bot.polling(non_stop=True)
