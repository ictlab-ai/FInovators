from flask import Flask, request, jsonify
import subprocess
import os

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/health", methods=["GET"])
def health():
    return {"status": "ok"}

@app.route("/ocr", methods=["POST"])
def ocr_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    output_file = filepath + ".txt"

    ext = file.filename.lower().split('.')[-1]
    # Если PDF, конвертируем в PNG
    if ext == "pdf":
        png_file = filepath + ".png"
        subprocess.run(["convert", "-density", "300", filepath, png_file], check=True)
        input_file = png_file
    else:
        input_file = filepath

    # Запускаем Cuneiform
    cmd = ["cuneiform", "-l", "rus+eng", "-o", output_file, input_file]
    result = subprocess.run(cmd, capture_output=True)

    if os.path.exists(output_file):
        with open(output_file, "r", encoding="utf-8") as f:
            text = f.read()
        return jsonify({"text": text})
    else:
        return jsonify({"error": "OCR failed", "stderr": result.stderr.decode()}), 500

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
