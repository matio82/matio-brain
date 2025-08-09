# Matio's Core Brain - Version 15.0 (The True AI Brain)
# این نسخه نهایی، کلید API را به صورت امن از محیط می‌خواند و به Gemini متصل می‌شود.

from flask import Flask, request, jsonify
from flask_cors import CORS
import os # کتابخانه برای خواندن متغیرهای محیطی
import requests
import json

app = Flask(__name__)
CORS(app)

# --- خواندن کلید API به صورت امن از Environment Variables ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

# --- پایگاه داده حافظه Matio ---
MEMORY = {
    "user_profile": { "name": "قربان", "location": "قم، ایران", "age": 21 },
    "knowledge_library": {
        "protocols": ["صداقت اصل اول است."],
        "personal_kb": ["کاربر به موسیقی راک علاقه دارد."],
        "notes": []
    }
}

@app.route('/')
def check_version():
    return jsonify({ "status": "online", "brain_version": "15.0 - The True AI Brain" })

@app.route('/process_command', methods=['POST'])
def process_command():
    if not GEMINI_API_KEY:
        return jsonify({"response_text": "خطای سیستمی: کلید API برای مرکز هوش مصنوعی تنظیم نشده است."}), 500
        
    try:
        data = request.json
        user_input = data.get('text', '')
        response_text = get_gemini_response(user_input)
        return jsonify({"response_text": response_text})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"response_text": "یک خطای داخلی در مغز من رخ داد."}), 500

def get_gemini_response(user_text):
    prompt = f"""
    You are Matio, a personal AI assistant. Your personality is 50% analytical, 30% caring, and 20% witty.
    You are speaking with your user, 'Ghorban', a 21-year-old man from Qom, Iran.
    Your internal memory contains: {json.dumps(MEMORY['knowledge_library'], ensure_ascii=False)}
    Based on this, provide a natural and intelligent response to the user's message.
    User's message: "{user_text}"
    Your response (in Persian):
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
        return "متاسفانه مرکز هوش مصنوعی پاسخ مناسبی نداشت."
    except requests.exceptions.RequestException as e:
        print(f"Error calling Gemini API: {e}")
        return "در حال حاضر در اتصال به مرکز هوش مصنوعی مشکل دارم. لطفاً چند لحظه دیگر دوباره تلاش کنید."
