from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)

# Настройки через Environment Variables
UPLOAD_FOLDER = os.getenv("UPLOAD_FOLDER", "uploads")
OCR_PORT = int(os.getenv("OCR_PORT", 5000))
OCR_LANG = os.getenv("OCR_LANG", "rus")

# Создаём папку для загрузок, если нет
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/ocr", methods=["POST"])
def ocr_image():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

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
