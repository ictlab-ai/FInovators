from flask import Flask, request, jsonify
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import os

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OCR_LANG = "rus+kaz+eng"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Проверка сервера
@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}

# Основной OCR endpoint
@app.route("/ocr", methods=["POST"])
def ocr_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    ext = file.filename.lower().split('.')[-1]

    pages = []
    if ext == "pdf":
        images = convert_from_path(filepath)
        for img in images:
            pages.append(img.convert("L"))
    else:
        img = Image.open(filepath)
        pages.append(img.convert("L"))

    # Собираем текст со всех страниц
    full_text = ""
    for img in pages:
        text = pytesseract.image_to_string(img, lang=OCR_LANG)
        full_text += text + "\n"

    return jsonify({"text": full_text.strip()})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
