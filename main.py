import telebot
import requests
from flask import Flask
import threading
import os

# ⚠️ NAYI GOOGLE API KEY YAHAN DALEIN (Single quotes ke andar)
GEMINI_API_KEY = 'AQ.Ab8RN6LgdSu23IZ-ehcb-Yscx72gV05xP3ZwMel11RH2LGOxWA'

# ⚠️ TELEGRAM BOT TOKEN YAHAN DALEIN
BOT_TOKEN = '9110746197:AAGtnkUta1T8JxN1RXe1kCVFes3Xti1q0gc'

bot = telebot.TeleBot(BOT_TOKEN)

# 🌐 1. RESEARCH FEATURE (Google Gemini AI URL 100% Correct)
def ask_gemini(prompt):
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"
    headers = {'Content-Type': 'application/json'}
    data = {
        "contents": [{
            "parts": [{"text": prompt + " (Please reply in brief and helpful Hindi or English as asked)"}]
        }]
    }
    try:
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            result = response.json()
            return result['candidates'][0]['content']['parts'][0]['text']
        else:
            return "Sorry, Gemini AI se connect karne mein dikkat aa rahi hai."
    except Exception as e:
        return f"Error: {str(e)}"

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
    bot.infinity_polling(skip_pending=True)
    
