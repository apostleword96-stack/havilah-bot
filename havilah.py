import os
import telebot
from groq import Groq

bot=telebot.TeleBot(os.getenv("TELEGRAM_TOKEN"))
ai=Groq(api_key=os.getenv("GROQ_API_KEY"))
MODE="CEO"

def ask(q):
 prompt="You are HAVILAH. Lagos Business CEO. Business: 1-on-1 coaching to get 10 clients in 30 days. RULE: Never say wellness. Only sales/clients/money. Format: ACTION: NEXT: CTA:. "+q
 r=ai.chat.completions.create(model="llama-3.1-70b-versatile",messages=[{"role":"user","content":prompt}],temperature=0.2)
 return r.choices[0].message.content

@bot.message_handler(func=lambda m:True)
def h(m):
 global MODE
 t=m.text.lower()
 if "smm" in t:MODE="SMM";bot.reply_to(m,"MODE: SMM ON")
 elif "sales" in t:MODE="SALES";bot.reply_to(m,"MODE: SALES ON")
 elif "post" in t:bot.reply_to(m,ask("Write 1 post to sell 10 clients coaching"))
 elif "dm" in t:bot.reply_to(m,ask("Write 1 cold DM to sell coaching"))
 else:bot.reply_to(m,ask(m.text))

bot.polling()
