import os
import tempfile
import subprocess
from flask import Flask, request, jsonify

app = Flask(__name__)

API_TOKEN = os.environ.get('OCR_API_TOKEN')

@app.route('/ocr', methods=['POST'])
def ocr():
    if API_TOKEN:
        token = request.headers.get('X-API-Token', '')
        if token != API_TOKEN:
            return jsonify({'error': 'unauthorized'}), 401

    if 'file' not in request.files:
        return jsonify({'error': 'no file uploaded'}), 400

    f = request.files['file']
    suffix = '.' + f.filename.rsplit('.', 1)[1].lower() if '.' in f.filename else '.png'
    tmp = tempfile.NamedTemporaryFile(delete=False, suffix=suffix)

    try:
        f.save(tmp.name)
        result = subprocess.run(['dots-ocr', tmp.name],
                                capture_output=True, text=True, timeout=120)
        if result.returncode != 0:
            return jsonify({'error': 'ocr_failed', 'stderr': result.stderr}), 500
        return jsonify({'text': result.stdout})
    finally:
        tmp.close()
        os.unlink(tmp.name)
