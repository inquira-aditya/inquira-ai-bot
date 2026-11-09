import telebot
import requests
from flask import Flask
import threading
import os
import time
# ⚠️ NAYI GOOGLE API KEY YAHAN DALEIN (Single quotes ke andar)
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

# ⚠️ TELEGRAM BOT TOKEN YAHAN DALEIN
BOT_TOKEN = os.getenv("BOT_TOKEN")

bot = telebot.TeleBot(BOT_TOKEN)

# 🌐 1. RESEARCH FEATURE (Google Gemini AI URL 100% Correct)


def ask_gemini(prompt):
    models = ["gemini-flash-latest", "gemini-flash-lite-latest"]
    headers = {'Content-Type': 'application/json'}
    data = {"contents": [{"parts": [{"text": prompt + " (Please reply in brief and helpful Hindi or English as asked)"}]}]}
    for model in models:
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={GEMINI_API_KEY}"
        for attempt in range(2):
            try:
                response = requests.post(url, headers=headers, json=data, timeout=30)
                if response.status_code == 200:
                    return response.json()['candidates'][0]['content']['parts'][0]['text']
                if response.status_code in (429, 500, 503):
                    time.sleep(2)
                    continue
                break
            except Exception as e:
                time.sleep(2)
    return "Gemini abhi busy hai, 1 minute baad dobara try karo."

# 📩 Telegram Messages ko Handle karna
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_text = message.text
    chat_id = message.chat.id
    
    if user_text.startswith('/photo '):
        prompt = user_text.replace('/photo ', '')
        bot.send_message(chat_id, "🔍 Aapki photo generate ho rahi hai...")
        image_url = f"https://pollinations.ai{requests.utils.quote(prompt)}?width=1024&height=1024&nologo=true"
        try:
            bot.send_photo(chat_id, image_url)
        except Exception as e:
            bot.send_message(chat_id, "Photo banane mein koi error aaya.")
    else:
        bot.send_message(chat_id, "🧠 Researching... Thoda samay dein...")
        ai_reply = ask_gemini(user_text)
        bot.send_message(chat_id, ai_reply)

# 🏢 2. RENDER FREE SERVER BYPASS (Flask App)
app = Flask('')

@app.route('/')
def home():
    return "Inquira AI Bot is Live 24/7!"

def run_flask():
    port = int(os.environ.get("PORT", 8080))
    app.run(host='0.0.0.0', port=port)

# Both servers ko ek sath chalu karna
if __name__ == "__main__":
    t = threading.Thread(target=run_flask)
    t.start()
    print("🚀 Aapka AI Bot active ho gaya hai!")
    while True:
        try:
            bot.infinity_polling(skip_pending=True, timeout=20, long_polling_timeout=20)
        except Exception as e:
            print("Polling error:", e, flush=True)
            time.sleep(10)    
    
