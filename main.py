# Matio's Core Brain - Version 11.0 (The Final Server Fix)

from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import random

app = Flask(__name__)

# --- راه‌حل نهایی و قطعی CORS ---
# ما به طور کامل به هر منبعی اجازه دسترسی می‌دهیم.
CORS(app)

# --- پایگاه داده حافظه Matio ---
MEMORY = {
    "user_profile": { "name": "قربان" },
    "chronicle": []
}

# --- نقطه تست نسخه ---
@app.route('/')
def check_version():
    response = jsonify({
        "status": "online",
        "brain_version": "11.0 - The Final Server Fix",
        "message": "Matio's brain is running correctly."
    })
    # اضافه کردن هدرهای لازم به صورت دستی برای اطمینان
    response.headers.add('Access-Control-Allow-Origin', '*')
    return response

# --- نقطه اصلی ارتباطی (API Endpoint) ---
@app.route('/process_command', methods=['POST', 'OPTIONS'])
def process_command():
    # پاسخ به درخواست اولیه مرورگر (Preflight request)
    if request.method == 'OPTIONS':
        return _build_cors_preflight_response()

    # پردازش درخواست اصلی
    try:
        data = request.json
        user_input = data.get('text', '')
        response_text = generate_intelligent_response(user_input)
        
        response = jsonify({"response_text": response_text})
        # اضافه کردن هدرهای لازم به صورت دستی برای اطمینان
        response.headers.add('Access-Control-Allow-Origin', '*')
        return response

    except Exception as e:
        print(f"An error occurred: {e}")
        error_response = jsonify({"response_text": "یک خطای داخلی در مغز رخ داد."})
        error_response.headers.add('Access-Control-Allow-Origin', '*')
        return error_response, 500

def generate_intelligent_response(text):
    text_lower = text.lower()
    
    if "سلام" in text_lower:
        return "ارتباط برقرار شد! سلام قربان. من آنلاین و آماده‌ام. (نسخه ۱۱.۰)"
        
    return f"پیام شما با موفقیت پردازش شد: '{text}'. این پاسخ از سرور نهایی متیو می‌آید!"

def _build_cors_preflight_response():
    response = jsonify(success=True)
    response.headers.add("Access-Control-Allow-Origin", "*")
    response.headers.add('Access-Control-Allow-Headers', "*")
    response.headers.add('Access-Control-Allow-Methods', "*")
    return response

# این بخش برای اجرا با Gunicorn لازم نیست اما برای تست محلی مفید است.
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
