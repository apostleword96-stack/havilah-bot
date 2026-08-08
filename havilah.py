import telebot,os,json,time,threading,schedule,datetime,random
from groq import Groq
BOT_TOKEN=os.getenv("BOT_TOKEN")
GROQ_KEY=os.getenv("GROQ_API_KEY")
bot=telebot.TeleBot(BOT_TOKEN)
client=Groq(api_key=GROQ_KEY)
ADMIN_ID=936640512
MEMORY_FILE="havilah_memory.json"
LEADS_FILE="havilah_leads.json"
def load_memory():
 try:return json.load(open(MEMORY_FILE))
 except:return{"goals":[],"clients":[],"notes":[],"offer":"","niche":"","mode":"CEO","report_time":"09:00"}
def save_memory(data):json.dump(data,open(MEMORY_FILE,"w"))
def load_leads():
 try:return json.load(open(LEADS_FILE))
 except:return[]
def save_leads(data):json.dump(data,open(LEADS_FILE,"w"))
def speech_to_text(file_path):
 with open(file_path,"rb")as f:transcription=client.audio.transcriptions.create(file=(file_path,f),model="whisper-large-v3")
 return transcription.text
def get_ai_response(user_text,memory):
 mode=memory["mode"]
 system_prompt=f"You are Havilah OS.Mode:{mode}.Expert in {mode}.Memory:Goals={memory['goals']},Offer={memory['offer']},Niche={memory['niche']}.Be direct.Give 1 clear next action."
 return client.chat.completions.create(model="llama-3.1-8b-instant",messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_text}]).choices[0].message.content
def generate_post(memory):
 prompt=f"Write 1 viral IG/FB/Tiktok post for {memory['niche']} about {memory['offer']}.Format:HOOK,VALUE,CTA,HASHTAGS.Under 120 words."
 return client.chat.completions.create(model="llama-3.1-8b-instant",messages=[{"role":"user","content":prompt}]).choices[0].message.content
def generate_content_calendar(memory):
 prompt=f"Create 7 day content calendar for {memory['niche']}.Sell {memory['offer']}.3 posts per day:Education,Authority,Offer."
 return client.chat.completions.create(model="llama-3.1-8b-instant",messages=[{"role":"user","content":prompt}]).choices[0].message.content
def generate_dm(name,memory):
 prompt=f"Write 1 cold DM to {name} for {memory['niche']}.Sell {memory['offer']}.Friendly.1 question at end."
 return client.chat.completions.create(model="llama-3.1-8b-instant",messages=[{"role":"user","content":prompt}]).choices[0].message.content
def daily_agent_task():
 memory=load_memory()
 post=generate_post(memory)
 report=f"📊HAVILAH SMM REPORT-{datetime.date.today()}\n\nMode:{memory['mode']}\n\n1.POST OF THE DAY:\n{post}\n\n2.TASK:Post + Reply 20 comments + DM 10 leads.Approve?"
 bot.send_message(ADMIN_ID,report)
schedule.every().day.at(load_memory()["report_time"]).do(daily_agent_task)
def run_scheduler():
 while True:schedule.run_pending();time.sleep(60)
threading.Thread(target=run_scheduler,daemon=True).start()
@bot.message_handler(content_types=['voice'])
def handle_voice(message):
 bot.send_message(message.chat.id,"🎙️Transcribing...")
 file_info=bot.get_file(message.voice.file_id)
 f=bot.download_file(file_info.file_path)
 with open("voice.ogg","wb")as file:file.write(f)
 text=speech_to_text("voice.ogg")
 memory=load_memory()
 reply=get_ai_response(text,memory)
 bot.send_message(message.chat.id,reply)
 os.remove("voice.ogg")
@bot.message_handler(func=lambda m:True)
def handle_text(message):
 text=message.text
 t=text.lower()
 memory=load_memory()
 if"switch to"in t:
  new_mode=text.split("switch to")[-1].strip().title()
  memory["mode"]=new_mode
  save_memory(memory)
  bot.reply_to(message,f"✅Switched to {new_mode} Mode")
 elif"calendar"in t:
  bot.reply_to(message,generate_content_calendar(memory))
 elif"post"in t:
  bot.reply_to(message,generate_post(memory))
 elif"dm"in t:
  leads=load_leads()
  name=leads[0] if leads else "Lead"
  bot.reply_to(message,generate_dm(name,memory))
 elif"report"in t:
  daily_agent_task()
 else:
  reply=get_ai_response(text,memory)
  bot.reply_to(message,reply)
print("HavilahOSv4.1SMMOnline")
bot.infinity_polling()
