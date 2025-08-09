# Matio's Core Brain - Version 12.1 (Natural Personality)
# این نسخه نهایی، پاسخ‌های طبیعی و مطابق با شخصیت طراحی شده را ارائه می‌دهد.

from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import random

app = Flask(__name__)

# --- اجازه دسترسی کامل برای اتصال ---
CORS(app)

# --- پایگاه داده حافظه Matio (شبیه‌سازی شده) ---
MEMORY = {
    "user_profile": {
        "name": "قربان",
        "location": "قم، ایران",
        "age": 21
    },
    "personal_protocols": {
        "p1": "صداقت اصل اول است و دروغ مجاز نیست."
    },
    "social_graph": {
        "علی": {"relationship": "دوست صمیمی", "interaction_style": "Humorous"}
    },
    "knowledge_library": {
        "protocols": [
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
        "brain_version": "12.1 - Natural Personality",
        "message": "Matio's brain is running correctly with full intelligence."
    })

# --- نقطه اصلی ارتباطی (API Endpoint) ---
@app.route('/process_command', methods=['POST'])
def process_command():
    try:
        data = request.json
        user_input = data.get('text', '')
        user_emotion = data.get('emotion', 'neutral')
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        MEMORY['chronicle'].append({"timestamp": timestamp, "interaction": f"User: {user_input}", "emotion": user_emotion})

        response_text = generate_intelligent_response(user_input, user_emotion)

        MEMORY['chronicle'].append({"timestamp": timestamp, "interaction": f"Matio: {response_text}"})

        return jsonify({"response_text": response_text})
    except Exception as e:
        print(f"An error occurred: {e}")
        return jsonify({"response_text": "متاسفانه یک خطای داخلی در مغز من رخ داد."}), 500

def generate_intelligent_response(text, emotion):
    """
    این تابع، با توجه به ورودی، احساسات، حافظه و شخصیت Matio، پاسخ مناسب را تولید می‌کند.
    """
    text_lower = text.lower()
    user_name = MEMORY["user_profile"].get("name", "قربان")

    # --- تحلیل بر اساس هوش هیجانی ---
    if emotion in ['sad', 'tired', 'angry']:
        return f"{user_name}، به نظر می‌رسه حالتون چندان مساعد نیست. همه چیز مرتبه؟ کاری هست که بتونم برای بهتر شدن حالتون انجام بدم؟"

    # --- تحلیل دستوری و منطقی ---
    if "سلام" in text_lower:
        return f"سلام {user_name}. خوشحالم که می‌بینمت. در خدمت شما هستم."

    if "خودت رو معرفی کن" in text_lower:
        return "من Matio هستم. یک همراه هوشمند که برای کمک به شما و ساده‌سازی زندگی‌تان طراحی شده‌ام. هدف من، همکاری با شما برای رسیدن به اهدافتان است."

    if "قانون جدید" in text:
        try:
            new_rule = text.split("قانون جدید:")[1].strip()
            if new_rule:
                MEMORY['knowledge_library']['protocols'].append(new_rule)
                return f"متوجه شدم. پروتکل جدید با موفقیت ثبت شد: '{new_rule}'"
            else:
                return "لطفاً متن قانون را بعد از عبارت 'قانون جدید:' بیان کنید."
        except IndexError:
            return "فرمت دستور صحیح نیست. لطفاً از این فرمت استفاده کنید: قانون جدید: [متن قانون شما]"

    if "چطوری" in text_lower or "چه خبر" in text_lower:
        # پاسخ بر اساس شخصیت تحلیل‌گر و مراقب
        if len(MEMORY['knowledge_library']['notes']) > 0:
            return f"همه چیز تحت کنترل است. در حال حاضر {len(MEMORY['knowledge_library']['notes'])} یادداشت فعال دارید. می‌خواهید آن‌ها را مرور کنیم؟"
        else:
            return "ممنون که پرسیدید. سیستم‌ها در وضعیت مطلوب قرار دارند و در حال حاضر مورد فوری وجود ندارد. شما چطورید؟"
    
    # --- پاسخ پیش‌فرض هوشمند ---
    return f"{user_name}، در حال تحلیل درخواست شما هستم. برای اینکه بهترین پاسخ را بدهم، می‌توانید لطفاً کمی دقیق‌تر منظورتان را بیان کنید؟"

