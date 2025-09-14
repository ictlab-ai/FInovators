import os
from flask import Flask, request, jsonify
import dots.ocr as dots

app = Flask(__name__)

API_TOKEN = os.environ.get("OCR_API_TOKEN")  # если не задан, API будет открытым

@app.route("/ocr", methods=["POST"])
def ocr():
    # Проверка токена (если установлен)
    if API_TOKEN:
        token = request.headers.get("X-API-Token", "")
        if token != API_TOKEN:
            return jsonify({"error": "unauthorized"}), 401

    # Проверка файла
    if "file" not in request.files:
        return jsonify({"error": "no file uploaded"}), 400

    f = request.files["file"]
    try:
        text = dots.read(f.stream)
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": "ocr_failed", "details": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
