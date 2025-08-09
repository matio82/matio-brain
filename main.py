# Matio's Core Brain - Version 3.0 (With Memory API)
# این نسخه قابلیت مدیریت حافظه از راه دور را دارد.

from flask import Flask, request, jsonify
from flask_cors import CORS
import datetime
import random

app = Flask(__name__)
CORS(app)

# --- پایگاه داده حافظه Matio (حالا این حافظه واقعی است) ---
MEMORY = {
    "userName": "قربان",
    "knowledge_library": {
        "protocols": ["صداقت اصل اول است.", "هرگز اطلاعات مالی را صوتی نخوان."],
        "personal_kb": ["به موسیقی راک علاقه دارد."],
        "notes": ["لیست خرید: شیر، نان", "تماس با علی"]
    },
}

# --- نقطه اصلی ارتباطی برای چت ---
@app.route('/process_command', methods=['POST'])
def process_command():
    data = request.json
    user_input = data.get('text', '')
    response_text = generate_simulated_response(user_input)
    return jsonify({"response_text": response_text})

# --- API های جدید برای مدیریت حافظه ---
@app.route('/memory', methods=['GET'])
def get_memory():
    return jsonify(MEMORY['knowledge_library'])

@app.route('/memory/add', methods=['POST'])
def add_memory_item():
    data = request.json
    category = data.get('category')
    item = data.get('item')
    if category and item and category in MEMORY['knowledge_library']:
        MEMORY['knowledge_library'][category].append(item)
        return jsonify({"status": "success", "message": "آیتم با موفقیت اضافه شد."})
    return jsonify({"status": "error", "message": "اطلاعات ناقص یا دسته‌بندی نامعتبر است."}), 400

@app.route('/memory/delete', methods=['POST'])
def delete_memory_item():
    data = request.json
    category = data.get('category')
    index = data.get('index')
    if category and isinstance(index, int) and category in MEMORY['knowledge_library']:
        try:
            del MEMORY['knowledge_library'][category][index]
            return jsonify({"status": "success", "message": "آیتم با موفقیت حذف شد."})
        except IndexError:
            return jsonify({"status": "error", "message": "اندیس نامعتبر است."}), 400
    return jsonify({"status": "error", "message": "اطلاعات ناقص یا دسته‌بندی نامعتبر است."}), 400


def generate_simulated_response(text):
    text_lower = text.lower()
    # ... (منطق پاسخگویی مانند قبل باقی می‌ماند) ...
    if "سلام" in text_lower: return f"سلام {MEMORY['userName']} عزیز. خوشحالم که می‌بینمت."
    if "اسم من" in text_lower:
        name = text.split(" ").pop().replace(".", "")
        MEMORY['userName'] = name
        return f"از آشنایی با شما خوشبختم {name} عزیز. اسمت رو به خاطر می‌سپارم."
    if "من کیم" in text_lower: return f"البته. شما {MEMORY['userName']} هستید. درسته؟"
    
    # حالا پاسخ‌ها می‌توانند از حافظه واقعی استفاده کنند
    if "یادداشت" in text_lower and "دارم" in text_lower:
        note_count = len(MEMORY['knowledge_library']['notes'])
        return f"بله، در حال حاضر {note_count} یادداشت در حافظه من ثبت شده است."

    return "متوجه منظورت شدم. چطور می‌تونم کمکت کنم؟"

