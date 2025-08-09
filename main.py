# Matio's Core Brain - Version 3.1 (Professional Grade by User)
# این نسخه شامل بهبودهای حرفه‌ای مانند لاگ، اعتبارسنجی و مدیریت خطاست.

import re
import logging
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
# نکته: این تنظیمات CORS برای استقرار نهایی باید تغییر کند تا آدرس اپلیکیشن شما را شامل شود.
CORS(app) 

# تنظیم logging
logging.basicConfig(level=logging.INFO)

# --- پایگاه داده حافظه Matio ---
MEMORY = {
    "user_name": "قربان",
    "knowledge_library": {
        "protocols": ["صداقت اصل اول است.", "هرگز اطلاعات مالی را صوتی نخوان."],
        "personal_kb": ["به موسیقی راک علاقه دارد."],
        "notes": ["لیست خرید: شیر، نان", "تماس با علی"]
    },
}

# --- نقطه اصلی ارتباطی برای چت ---
@app.route('/process_command', methods=['POST'])
def process_command():
    try:
        data = request.json
        user_input = data.get('text', '')
        if not user_input:
            return jsonify({"error": "ورودی متن الزامی است."}), 400
        response_text = generate_simulated_response(user_input)
        return jsonify({"response_text": response_text})
    except Exception as e:
        logging.error(f"Error in process_command: {str(e)}")
        return jsonify({"error": "خطا در پردازش درخواست."}), 500

# --- API های جدید برای مدیریت حافظه ---
@app.route('/memory', methods=['GET'])
def get_memory():
    return jsonify(MEMORY['knowledge_library'])

@app.route('/memory/add', methods=['POST'])
def add_memory_item():
    try:
        data = request.json
        category = data.get('category')
        item = data.get('item')
        if not category or not item:
            return jsonify({"status": "error", "message": "اطلاعات ناقص است."}), 400
        if not isinstance(item, str) or len(item) > 500:
            return jsonify({"status": "error", "message": "آیتم نامعتبر است."}), 400
        if category not in MEMORY['knowledge_library']:
            MEMORY['knowledge_library'][category] = []
        MEMORY['knowledge_library'][category].append(item)
        logging.info(f"Added item to {category}: {item}")
        return jsonify({"status": "success", "message": "آیتم با موفقیت اضافه شد."})
    except Exception as e:
        logging.error(f"Error in add_memory_item: {str(e)}")
        return jsonify({"status": "error", "message": "خطا در افزودن آیتم."}), 500

@app.route('/memory/delete', methods=['POST'])
def delete_memory_item():
    try:
        data = request.json
        category = data.get('category')
        index = data.get('index')
        if not category or not isinstance(index, int):
            return jsonify({"status": "error", "message": "اطلاعات ناقص یا نامعتبر است."}), 400
        if category not in MEMORY['knowledge_library']:
            return jsonify({"status": "error", "message": "دسته‌بندی نامعتبر است."}), 400
        if not (0 <= index < len(MEMORY['knowledge_library'][category])):
            return jsonify({"status": "error", "message": "اندیس نامعتبر است."}), 400
        deleted_item = MEMORY['knowledge_library'][category].pop(index)
        logging.info(f"Deleted item from {category}: {deleted_item}")
        return jsonify({"status": "success", "message": "آیتم با موفقیت حذف شد."})
    except Exception as e:
        logging.error(f"Error in delete_memory_item: {str(e)}")
        return jsonify({"status": "error", "message": "خطا در حذف آیتم."}), 500

def generate_simulated_response(text):
    text_lower = text.lower()
    
    if "سلام" in text_lower:
        return f"سلام {MEMORY['user_name']} عزیز. خوشحالم که می‌بینمت."
    
    if "اسم من" in text_lower:
        name_match = re.search(r"اسم من ([\w]+)", text)
        if name_match:
            new_name = name_match.group(1)
            MEMORY['user_name'] = new_name
            return f"از آشنایی با شما خوشبختم {new_name} عزیز. اسمت رو به خاطر می‌سپارم."
        return "متوجه نام شما نشدم. لطفاً دوباره بگویید."
    
    if "من کیم" in text_lower:
        return f"البته. شما {MEMORY['user_name']} هستید. درسته؟"
    
    if "یادداشت" in text_lower and "دارم" in text_lower:
        note_count = len(MEMORY['knowledge_library']['notes'])
        return f"بله، در حال حاضر {note_count} یادداشت در حافظه من ثبت شده است."
    
    if "یادداشت" in text_lower and ("لیست" in text_lower or "چی" in text_lower):
        notes = MEMORY['knowledge_library']['notes']
        if notes:
            return f"یادداشت‌های شما: {', '.join(notes)}"
        return "هیچ یادداشتی ثبت نشده است."
    
    return "متوجه منظورت شدم. چطور می‌تونم کمکت کنم؟"

# این بخش برای اجرای سرور در Render با Gunicorn استفاده نخواهد شد، اما برای تست محلی عالی است.
if __name__ == '__main__':
    app.run(debug=True)
