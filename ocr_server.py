from flask import Flask, request, jsonify
import subprocess
import os
from PIL import Image

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OCR_PORT = 5000

# Языки для распознавания
OCR_LANG = "rus+kaz+eng"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Главная страница для проверки ---
@app.route("/", methods=["GET"])
def index():
    return "OCR сервер работает. Для распознавания используйте POST на /ocr"

# --- Эндпоинт для распознавания ---
@app.route("/ocr", methods=["POST"])
def ocr_image():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Конвертация изображения в ч/б PNG
    try:
        img = Image.open(filepath)
        img = img.convert("L")  # оттенки серого
        bw_path = os.path.splitext(filepath)[0] + "_bw.png"
        img.save(bw_path)
        filepath = bw_path
    except Exception as e:
        return jsonify({"error": f"Image conversion failed: {e}"}), 500

    # Запуск Cuneiform
    try:
        result = subprocess.run(
            ["cuneiform", "-l", OCR_LANG, "-f", "text", filepath],
            capture_output=True,
            text=True
        )
        text = result.stdout.strip()
        if not text:
            text = "[Cuneiform не распознал текст]"
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=OCR_PORT)
