from flask import Flask, request, jsonify
import subprocess
import os
from PIL import Image  # для конвертации в ч/б

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OCR_PORT = 5000

# Языки: русский, казахский, английский
OCR_LANG = "rus+kaz+eng"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/ocr", methods=["POST"])
def ocr_image():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Конвертируем изображение в ч/б PNG
    try:
        img = Image.open(filepath)
        img = img.convert("L")
        bw_path = os.path.splitext(filepath)[0] + "_bw.png"
        img.save(bw_path)
        filepath = bw_path
    except Exception as e:
        return jsonify({"error": f"Image conversion failed: {e}"}), 500

    # Запускаем Cuneiform
    try:
        result = subprocess.run(
            ["cuneiform", "-l", OCR_LANG, "-f", "text", filepath],
            capture_output=True,
            text=True
        )
        text = result.stdout
        return jsonify({"text": text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=OCR_PORT)
