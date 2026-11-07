import telebot
import requests

# ⚠️ APNI GOOGLE API KEY YAHAN DALEIN
# Jo API Key aapko Google AI Studio se mili hai (Nov 3 wali), use niche ' ' ke andar paste karein
GEMINI_API_KEY = 'AQ.Ab8RN6L34JlUKvcwXRXvOjyp7hfi1-zhBEV2KHZdoH_KR43tQg'

# ⚠️ TELEGRAM BOT TOKEN (Ise hum baad mein dalein ge jab restriction hategi)
BOT_TOKEN = '9110746197:AAGtnkUta1T8JxN1RXe1kCVFes3Xtilq0gcmain.py'

bot = telebot.TeleBot(BOT_TOKEN)

# 🌐 1. RESEARCH FEATURE (Google Gemini AI)
def ask_gemini(prompt):
    url = f"https://googleapis.com{GEMINI_API_KEY}"
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
            return "Sorry, Gemini AI se connect karne mein dikkat aa rahi hai. Apni API key check karein."
    except Exception as e:
        return f"Error: {str(e)}"

# 📩 Telegram Messages ko Handle karna
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    user_text = message.text
    chat_id = message.chat.id
    
    # 🎨 2. PHOTO GENERATOR FEATURE (Agar message '/photo' se shuru ho)
    if user_text.startswith('/photo '):
        prompt = user_text.replace('/photo ', '')
        bot.send_message(chat_id, "🔍 Aapki photo generate ho rahi hai, thoda intezar karein...")
        
        # Real-world Free Image API (Pollinations)
        image_url = f"https://pollinations.ai{requests.utils.quote(prompt)}?width=1024&height=1024&nologo=true"
        
        try:
            bot.send_photo(chat_id, image_url)
        except Exception as e:
            bot.send_message(chat_id, "Photo banane mein koi error aaya. Dobara try karein.")
            
    else:
        # Agar normal text hai, to Gemini Research Assistant jawab dega
        bot.send_message(chat_id, "🧠 Researching... Thoda samay dein...")
        ai_reply = ask_gemini(user_text)
        bot.send_message(chat_id, ai_reply)

print("🚀 Aapka AI Bot active ho gaya hai! Telegram par jaakar test karein.")
bot.infinity_polling()
      
