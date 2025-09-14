from flask import Flask, request, jsonify
import os
from PIL import Image
import pytesseract

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OCR_LANG = "rus+kaz+eng"
OCR_PORT = 5000

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# --- Главная страница ---
@app.route("/", methods=["GET"])
def index():
    return "Tesseract OCR сервер работает. Для распознавания используйте POST на /ocr"

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
    except Exception as e:
        return jsonify({"error": f"Image conversion failed: {e}"}), 500

    try:
        # Распознаем текст через Tesseract
        text = pytesseract.image_to_string(img, lang=OCR_LANG)
        text = text.strip()
        if not text:
            text = "[Tesseract не распознал текст]"
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# --- Список поддерживаемых языков ---
@app.route("/langs", methods=["GET"])
def langs():
    try:
        langs = pytesseract.get_languages()
        return "<pre>" + "\n".join(langs) + "</pre>"
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=OCR_PORT)
