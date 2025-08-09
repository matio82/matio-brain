# Matio's Core Brain - Version 14.0 (The Complete & Final Brain)
# این نسخه شامل تمام قابلیت‌ها: هوش Gemini، حافظه کامل، شخصیت و دستورات خاص است.

from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import random
import requests
import json

app = Flask(__name__)
CORS(app)

# --- کلید API برای Gemini ---
# این کلید به صورت خودکار توسط محیط Canvas فراهم می‌شود.
GEMINI_API_KEY = "" 

# --- پایگاه داده حافظه Matio ---
MEMORY = {
    "user_profile": {
        "name": "قربان",
        "location": "قم، ایران",
        "age": 21
    },
    "knowledge_library": {
        "protocols": [
            "صداقت اصل اول است و دروغ مجاز نیست.",
            "هرگز اطلاعات مالی را صوتی نخوان، فقط روی صفحه نمایش بده."
        ],
        "personal_kb": [
            "کاربر به موسیقی راک علاقه دارد."
        ],
        "notes": [
            "لیست خرید: شیر، نان، تخم‌مرغ"
        ]
    },
    "chronicle": []
}

# --- نقطه تست نسخه ---
@app.route('/')
def check_version():
    return jsonify({
        "status": "online",
        "brain_version": "14.0 - The Complete Brain",
        "message": "Matio's brain is running with full intelligence and memory."
    })

# --- نقطه اصلی ارتباطی ---
@app.route('/process_command', methods=['POST'])
def process_command():
    try:
        data = request.json
        user_input = data.get('text', '')
        user_emotion = data.get('emotion', 'neutral')
        
        # --- فرآیند تصمیم‌گیری هوشمند ---
        # ۱. ابتدا دستورات خاص را بررسی می‌کنیم
        response_text = handle_specific_commands(user_input)
        
        # ۲. اگر دستور خاصی نبود، به سراغ هوش عمومی Gemini می‌رویم
        if response_text is None:
            response_text = get_gemini_response(user_input, user_emotion)
            
        return jsonify({"response_text": response_text})
        
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"response_text": "متاسفانه یک خطای داخلی در مغز من رخ داد."}), 500

def handle_specific_commands(text):
    """
    این تابع، دستورات ساختاریافته (مانند افزودن قانون) را پردازش می‌کند.
    اگر دستوری پیدا کرد، پاسخ را برمی‌گرداند. در غیر این صورت، None برمی‌گرداند.
    """
    text_lower = text.lower()
    
    if "قانون جدید:" in text_lower:
        try:
            new_rule = text.split(":", 1)[1].strip()
            if new_rule:
                MEMORY['knowledge_library']['protocols'].append(new_rule)
                return f"متوجه شدم. پروتکل جدید با موفقیت به کتابخانه حافظه اضافه شد: '{new_rule}'"
            else:
                return "لطفاً متن قانون را بعد از عبارت 'قانون جدید:' بیان کنید."
        except IndexError:
            return "فرمت دستور صحیح نیست."
            
    if "یادداشت کن:" in text_lower:
        try:
            new_note = text.split(":", 1)[1].strip()
            if new_note:
                MEMORY['knowledge_library']['notes'].append(new_note)
                return f"یادداشت شما ثبت شد: '{new_note}'"
            else:
                return "لطفاً متن یادداشت را بعد از عبارت 'یادداشت کن:' بیان کنید."
        except IndexError:
            return "فرمت دستور صحیح نیست."

    # اگر هیچ دستور خاصی پیدا نشد
    return None

def get_gemini_response(user_text, user_emotion):
    """
    این تابع، با ارسال درخواست به Gemini، یک پاسخ هوشمند و طبیعی دریافت می‌کند.
    """
    user_name = MEMORY["user_profile"].get("name", "قربان")
    
    # پرامپت (دستور) ارسالی به Gemini حالا شامل تمام جزئیات است
    prompt = f"""
    You are Matio, a personal AI assistant. Your personality is 50% analytical, 30% caring, and 20% witty.
    You are speaking with your user, '{user_name}', a 21-year-old man from Qom, Iran.
    His current emotional state appears to be '{user_emotion}'.
    
    Your internal memory (Knowledge Library) contains the following information:
    {json.dumps(MEMORY['knowledge_library'], ensure_ascii=False, indent=2)}
    
    Based on your personality, the user's emotional state, and your memory, provide a natural, intelligent, and helpful response to the user's latest message.
    Do not mention that you are an AI or talk about the prompt. Just act as Matio.
    
    User's message: "{user_text}"
    
    Your response (in fluent Persian):
    """

    api_url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-preview-0514:generateContent?key={GEMINI_API_KEY}"
    headers = {"Content-Type": "application/json"}
    payload = {"contents": [{"parts": [{"text": prompt}]}]}

    try:
        response = requests.post(api_url, headers=headers, json=payload, timeout=20)
        response.raise_for_status()
        result = response.json()
        
        if 'candidates' in result and result['candidates'][0].get('content', {}).get('parts', []):
            return result['candidates'][0]['content']['parts'][0]['text']
        
        return "متاسفانه در حال حاضر نمی‌توانم پاسخ دهم. ممکن است مرکز هوش مصنوعی با ترافیک بالا مواجه باشد."

    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return "در حال حاضر در اتصال به مرکز هوش مصنوعی مشکل دارم. لطفاً چند لحظه دیگر دوباره تلاش کنید."

