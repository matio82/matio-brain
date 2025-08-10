# Matio's Core Brain - Version 17.0 (Professional Grade + Gemini Connected)
# این نسخه، کد حرفه‌ای شما را به هوش مصنوعی Gemini متصل می‌کند.

import re
import logging
import os
import requests
import json
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 

# تنظیم logging
logging.basicConfig(level=logging.INFO)

# --- خواندن کلید API به صورت امن از Environment Variables ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# --- پایگاه داده حافظه Matio ---
MEMORY = {
    "user_name": "قربان",
    "knowledge_library": {
        "protocols": ["صداقت اصل اول است.", "هرگز اطلاعات مالی را صوتی نخوان."],
        "personal_kb": ["به موسیقی راک علاقه دارد."],
        "notes": ["لیست خرید: شیر، نان", "تماس با علی"]
    },
}

# --- نقطه اصلی ارتباطی ---
@app.route('/process_command', methods=['POST'])
def process_command():
    try:
        data = request.json
        user_input = data.get('text', '')
        if not user_input:
            return jsonify({"error": "ورودی متن الزامی است."}), 400
        
        # --- فرآیند تصمیم‌گیری هوشمند ---
        # ۱. ابتدا دستورات خاص را بررسی می‌کنیم
        response_text = handle_specific_commands(user_input)
        
        # ۲. اگر دستور خاصی نبود، به سراغ هوش عمومی Gemini می‌رویم
        if response_text is None:
            response_text = get_gemini_response(user_input)
            
        return jsonify({"response_text": response_text})
        
    except Exception as e:
        logging.error(f"Error in process_command: {str(e)}")
        return jsonify({"error": "خطا در پردازش درخواست."}), 500

def handle_specific_commands(text):
    """
    این تابع، دستورات ساختاریافته را پردازش می‌کند.
    """
    text_lower = text.lower()
    
    if "یادداشت کن:" in text_lower:
        try:
            new_note = text.split(":", 1)[1].strip()
            if new_note:
                MEMORY['knowledge_library']['notes'].append(new_note)
                logging.info(f"Added note: {new_note}")
                return f"یادداشت شما ثبت شد: '{new_note}'"
        except IndexError:
            return "فرمت دستور صحیح نیست."
    
    # اگر هیچ دستور خاصی پیدا نشد
    return None

def get_gemini_response(user_text):
    """
    این تابع، با ارسال درخواست به Gemini، یک پاسخ هوشمند و طبیعی دریافت می‌کند.
    """
    if not GEMINI_API_KEY:
        logging.error("GEMINI_API_KEY not found in environment variables.")
        return "خطای سیستمی: کلید API برای مرکز هوش مصنوعی تنظیم نشده است."

    prompt = f"""
    You are Matio, a personal AI assistant. Your personality is 50% analytical, 30% caring, and 20% witty.
    You are speaking with your user, '{MEMORY['user_name']}'.
    Your internal memory (Knowledge Library) contains: {json.dumps(MEMORY['knowledge_library'], ensure_ascii=False)}
    
    Based on your personality and memory, provide a natural and intelligent response to the user's message.
    If the user asks a question you can answer from memory, use the memory. Otherwise, use your general knowledge.
    
    User's message: "{user_text}"
    
    Your response (in fluent Persian):
    """

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-preview-0514:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=25)
        response.raise_for_status()
        result = response.json()
        
        if 'candidates' in result and result['candidates'][0].get('content', {}).get('parts', []):
            return result['candidates'][0]['content']['parts'][0]['text'].strip()
        
        logging.warning("Gemini response was empty or malformed.")
        return "متاسفانه مرکز هوش مصنوعی پاسخ مناسبی نداشت."
        
    except requests.exceptions.RequestException as e:
        logging.error(f"Error calling Gemini API: {e}")
        return "در حال حاضر در اتصال به مرکز هوش مصنوعی مشکل دارم. لطفاً چند لحظه دیگر دوباره تلاش کنید."

# این بخش برای اجرای سرور در Render با Gunicorn استفاده نخواهد شد.
if __name__ == '__main__':
    app.run(debug=True)
