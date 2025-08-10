# Matio's Core Brain - Version 3.1 (Professional Grade by User)
# این نسخه شامل بهبودهای حرفه‌ای مانند لاگ، اعتبارسنجی و مدیریت خطاست.

import os
import re
import json
import logging
from logging.handlers import RotatingFileHandler
from typing import Any, Dict, List, Optional
from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
from functools import wraps
from time import time

# ---------- تنظیمات پایه ----------
APP_NAME = "matio_core_brain"
DEBUG = os.getenv('FLASK_ENV', 'development') == 'development'
CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')  # در تولید حتما مقداردهی کنید
MEMORY_FILE = os.getenv('MEMORY_FILE', './memory.json')
EXTERNAL_AI_URL = os.getenv('EXTERNAL_AI_URL')  # مثال: Gemini endpoint
EXTERNAL_AI_KEY = os.getenv('EXTERNAL_AI_KEY')
EXTERNAL_AI_TIMEOUT = float(os.getenv('EXTERNAL_AI_TIMEOUT', '10'))

# محدودیت‌ها
MAX_ITEM_LENGTH = 500
ALLOWED_CATEGORIES = {'protocols', 'personal_kb', 'notes'}
RATE_LIMIT_WINDOW = 60  # ثانیه
RATE_LIMIT_MAX = 30  # درخواست در پنجره

# ---------- اپلیکیشن ----------
app = Flask(APP_NAME)

# CORS: در تولید بهتر است لیست مخصوص Origins قرار دهید
if CORS_ORIGINS.strip() == '*' or CORS_ORIGINS == '':
    CORS(app)
else:
    origins = [o.strip() for o in CORS_ORIGINS.split(',') if o.strip()]
    CORS(app, origins=origins)

# ---------- لاگینگ حرفه‌ای ----------
logger = logging.getLogger(APP_NAME)
logger.setLevel(logging.INFO if not DEBUG else logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

log_file = os.getenv('LOG_FILE', './matio_core_brain.log')
handler = RotatingFileHandler(log_file, maxBytes=5*1024*1024, backupCount=5)
handler.setFormatter(formatter)
logger.addHandler(handler)

# لاگ به کنسول هم برای محیط dev
if DEBUG:
    console = logging.StreamHandler()
    console.setFormatter(formatter)
    logger.addHandler(console)

# ---------- حافظه و عملیات ذخیره/بارگذاری ----------
DEFAULT_MEMORY = {
    "user_name": "قربان",
    "knowledge_library": {
        "protocols": ["صداقت اصل اول است.", "هرگز اطلاعات مالی را صوتی نخوان."],
        "personal_kb": ["به موسیقی راک علاقه دارد."],
        "notes": ["لیست خرید: شیر، نان", "تماس با علی"]
    }
}

_memory: Dict[str, Any] = {}

def load_memory() -> None:
    global _memory
    try:
        if os.path.exists(MEMORY_FILE):
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                _memory = json.load(f)
            logger.info(f"Memory loaded from {MEMORY_FILE}")
        else:
            _memory = DEFAULT_MEMORY.copy()
            persist_memory()
            logger.info("Initialized memory with defaults.")
    except Exception as e:
        logger.exception("Failed to load memory, using defaults.")
        _memory = DEFAULT_MEMORY.copy()

def persist_memory() -> None:
    try:
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(_memory, f, ensure_ascii=False, indent=2)
        logger.debug(f"Memory persisted to {MEMORY_FILE}")
    except Exception:
        logger.exception("Failed to persist memory to disk.")

# بارگذاری اولیه
load_memory()

# ... (بقیه کد هوشمندانه شما بدون تغییر باقی می‌ماند) ...

# ---------- پاسخ محلی امن و قابل گسترش ----------
def generate_simulated_response(text: str) -> str:
    text_lower = text.lower()
    
    if 'سلام' in text_lower:
        return f"سلام {_memory.get('user_name', 'دوست')} عزیز. خوشحالم که می‌بینمت."

    if 'اسم من' in text_lower:
        name_match = re.search(r"اسم من\s*[:\-]?\s*([\w؀-ۿ]+)", text)
        if name_match:
            new_name = name_match.group(1).strip()
            if new_name:
                _memory['user_name'] = new_name
                persist_memory()
                return f"از آشنایی با شما خوشبختم {new_name} عزیز. اسمت رو به خاطر می‌سپارم."
        return "متوجه نام شما نشدم. لطفاً دوباره بگویید."

    if 'من کیم' in text_lower or 'کی هستم' in text_lower:
        return f"شما {_memory.get('user_name', 'کاربر')} هستید."

    if 'یادداشت' in text_lower and 'دارم' in text_lower:
        notes = _memory.get('knowledge_library', {}).get('notes', [])
        note_count = len(notes)
        return f"بله، در حال حاضر {note_count} یادداشت در حافظه من ثبت شده است."

    if 'یادداشت' in text_lower and ('لیست' in text_lower or 'چی' in text_lower):
        notes = _memory.get('knowledge_library', {}).get('notes', [])
        if notes:
            return f"یادداشت‌های شما: {', '.join(notes)}"
        return "هیچ یادداشتی ثبت نشده است."

    return "متوجه منظورت شدم. چطور می‌تونم کمکت کنم؟"

# --- API های مدیریت حافظه (با بهبودهای شما) ---
@app.route('/memory', methods=['GET'])
def get_memory_api():
    return jsonify(_memory.get('knowledge_library', {}))

@app.route('/memory/add', methods=['POST'])
def add_memory_item_api():
    data = request.json
    category = data.get('category')
    item = data.get('item')
    if not category or not item or category not in ALLOWED_CATEGORIES:
        return jsonify({"status": "error", "message": "اطلاعات ناقص یا دسته‌بندی نامعتبر است."}), 400
    _memory['knowledge_library'][category].append(item)
    persist_memory()
    logger.info(f"Added item to {category}: {item}")
    return jsonify({"status": "success", "message": "آیتم با موفقیت اضافه شد."})

@app.route('/memory/delete', methods=['POST'])
def delete_memory_item_api():
    data = request.json
    category = data.get('category')
    index = data.get('index')
    if not category or not isinstance(index, int) or category not in ALLOWED_CATEGORIES:
        return jsonify({"status": "error", "message": "اطلاعات ناقص یا نامعتبر است."}), 400
    try:
        deleted_item = _memory['knowledge_library'][category].pop(index)
        persist_memory()
        logger.info(f"Deleted item from {category}: {deleted_item}")
        return jsonify({"status": "success", "message": "آیتم با موفقیت حذف شد."})
    except IndexError:
        return jsonify({"status": "error", "message": "اندیس نامعتبر است."}), 400

@app.route('/process_command', methods=['POST'])
def process_command_api():
    data = request.json
    user_input = data.get('text', '')
    response_text = generate_simulated_response(user_input)
    return jsonify({"response_text": response_text})


# ---------- اجرای محلی (برای توسعه) ----------
if __name__ == '__main__':
    logger.info(f"Starting {APP_NAME} (debug={DEBUG})")
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 5000)), debug=DEBUG)
