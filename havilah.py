import telebot,os,json,time,threading,schedule,datetime
from groq import Groq
BOT_TOKEN=os.getenv("BOT_TOKEN")
GROQ_KEY=os.getenv("GROQ_API_KEY")
bot=telebot.TeleBot(BOT_TOKEN)
client=Groq(api_key=GROQ_KEY)
ADMIN_ID=936640512
MEMORY_FILE="havilah_memory.json"
def load_memory():
 try:return json.load(open(MEMORY_FILE))
 except:return{"goals":[],"clients":[],"notes":[],"report_time":"09:00"}
def save_memory(data):json.dump(data,open(MEMORY_FILE,"w"))
def speech_to_text(file_path):
 with open(file_path,"rb")as f:transcription=client.audio.transcriptions.create(file=(file_path,f),model="whisper-large-v3")
 return transcription.text
def get_ai_response(user_text,memory):
 system_prompt=f"You are Havilah OS,proactive CEO Agent.Memory:Goals={memory['goals']},Clients={memory['clients']}.Be direct,strategic,suggest next action."
 return client.chat.completions.create(model="llama-3.1-8b-instant",messages=[{"role":"system","content":system_prompt},{"role":"user","content":user_text}]).choices[0].message.content
def daily_agent_task():
 memory=load_memory()
 report=f"📊HAVILAH REPORT-{datetime.date.today()}\nGoals:{memory['goals']}\nAction:Checked leads,drafted posts\nSuggestion:DM 10 new leads today.Approve?"
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
 bot.send_message(message.chat.id,f"You said:{text}")
 memory=load_memory()
 reply=get_ai_response(text,memory)
 bot.send_message(message.chat.id,reply)
 os.remove("voice.ogg")
@bot.message_handler(func=lambda m:True)
def handle_text(message):
 text=message.text.lower()
 memory=load_memory()
 if"remember"in text or"goal"in text:
  memory["goals"].append(message.text)
  save_memory(memory)
  bot.reply_to(message,"✅Saved to memory boss")
 elif"report"in text:
  daily_agent_task()
 else:
  reply=get_ai_response(message.text,memory)
  bot.reply_to(message,reply)
print("HavilahOSv2.1Online")
bot.infinity_polling()
