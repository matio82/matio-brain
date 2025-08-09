# Matio's Core Brain - Version 16.0 (API Key Test)
# این نسخه فقط برای تست خواندن کلید API از محیط Render طراحی شده است.

from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# --- تلاش برای خواندن کلید API از Environment Variables ---
GEMINI_API_KEY = os.environ.get('GEMINI_API_KEY')

@app.route('/')
def check_status():
    # در این بخش، ما مستقیماً وضعیت کلید را بررسی و گزارش می‌کنیم.
    if GEMINI_API_KEY and len(GEMINI_API_KEY) > 10:
        # اگر کلید وجود داشت و طولانی بود (یعنی احتمالاً معتبر است)
        status_message = "SUCCESS: The API key was found and read correctly."
        key_status = "Found and looks valid."
    else:
        # اگر کلید پیدا نشد یا خالی بود
        status_message = "FAILURE: The API key was NOT found or is empty."
        key_status = "Not Found!"

    return jsonify({
        "status": "online",
        "brain_version": "16.0 - API Key Test",
        "test_result": status_message,
        "gemini_api_key_status": key_status
    })

# ما بخش process_command را موقتاً غیرفعال می‌کنیم تا فقط روی تست تمرکز کنیم.
# @app.route('/process_command', ...)


