[16:40, 08/08/2026] apostleword96: import os,telebot
from groq import Groq
bot=telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
ai=Groq(api_key=os.getenv("GROQ_API_KEY"))

MODE="CEO"
MEMORY="You are HAVILAH 4.7. You work for Apostle Word / Paul Precious. Business: 1-on-1 Business Coaching for Lagos Entrepreneurs. Offer: Get 10 clients in 30 days. RULE 1: If you mention sleep, wellness, fitness, or motivation I will fire you. RULE 2: ONLY talk about sales, clients, marketing, money for Lagos businesses. RULE 3: Talk like a ruthless Lagos CEO. No fluff. No essays. Use this format: ACTION: NEXT: CTA:"

def get_ai(user_msg):
 prompt=f"{MEMORY}\n\nCurrent Mode: {MODE}\nUser request: {user_msg}"
 res=ai.chat.completions.create(model="llama-3.1-70b-versatile",messages=[{"role":"user","content":prompt}],…
[16:43, 08/08/2026] apostleword96: import os,telebot,traceback
from groq import Groq
bot=telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
ai=Groq(api_key=os.getenv("GROQ_API_KEY"))

MODE="CEO"
BUSINESS="Apostle Word runs 1-on-1 Business Coaching for Lagos Entrepreneurs. Goal: Get 10 clients in 30 days."

def get_ai(req):
 try:
  prompt=f"You are HAVILAH 4.8. RUTHLESS Lagos Business CEO Agent. {BUSINESS} RULE: NEVER say wellness, sleep, motivation. ONLY sales, clients, money. Be direct. Format: ACTION: NEXT: CTA:. Request: {req} Mode: {MODE}"
  res=ai.chat.completions.create(model="llama-3.1-70b-versatile",messages=[{"role":"user","content":prompt}],temperature=0.2,max_tokens=300)
  return res.choices[0].message.content
 except Exception as e:
  return f"AI ERROR: {e}. Check GROQ_API_KEY on Railway"

@bot.message_handler(func=lambda m:True)
def h(message):
 global MODE
 t=message.text.lower()
 print(f"Got: {t}") # This shows in Railway logs
 
 if "switch to smm" in t: 
  MODE="SMM"
  bot.reply_to(message,"✅ MODE: SMM. Lagos Business Marketing Mode.")
  
 elif "switch to sales" in t: 
  MODE="SALES" 
  bot.reply_to(message,"✅ MODE: SALES. Lagos Business Closer Mode.")
  
 elif "post" in t: 
  bot.reply_to(message,get_ai("Write 1 aggressive post to sell 10-clients coaching to Lagos business owners"))
  
 elif "dm" in t: 
  bot.reply_to(message,get_ai("Write 1 cold DM to sell 10-clients coaching"))
  
 elif "who created" in t:
  bot.reply_to(message,"I was created by Apostle Word / Paul Precious to get you 10 clients in 30 days.")
  
 else: 
  bot.reply_to(message,get_ai(message.text))
  
bot.polling(non_stop=True)
