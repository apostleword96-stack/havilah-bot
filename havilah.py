import os,telebot
from groq import Groq
bot=telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
ai=Groq(api_key=os.getenv("GROQ_API_KEY"))

BUSINESS="1-on-1 Business Coaching for Lagos Entrepreneurs. Goal: Get 10 clients in 30 days. Client: Apostle Word"
MODE="CEO"

def reply(user_msg):
 prompt=f"You are HAVILAH 4.4. Ruthless Lagos Business Agent. {BUSINESS}. MODE:{MODE}. RULES: 1.NO sleep/wellness 2.ONLY sales, clients, money 3.Be direct like CEO 4.Format: ACTION: NEXT: CTA:. User:{user_msg}"
 res=ai.chat.completions.create(model="llama-3.1-70b-versatile",messages=[{"role":"user","content":prompt}])
 return res.choices[0].message.content

@bot.message_handler(func=lambda m:True)
def h(m):
 global MODE
 t=m.text.lower()
 if "switch to smm" in t: MODE="SMM"; bot.reply(m,"MODE: SMM. Send 'post'")
 elif "switch to sales" in t: MODE="SALES"; bot.reply(m,"MODE: SALES. Send 'dm'")
 elif "post" in t: bot.reply(m,reply("Write 1 aggressive post to sell coaching to Lagos business owners"))
 elif "dm" in t: bot.reply(m,reply("Write 1 cold DM to sell my 10-clients offer"))
 else: bot.reply(m,"Commands: switch to SMM, switch to Sales, post, dm")
bot.polling()
