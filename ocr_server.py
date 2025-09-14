from flask import Flask, request, jsonify, send_file
import os
from PIL import Image
import pytesseract
from pdf2image import convert_from_path
import csv
import io

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
OCR_LANG = "rus+kaz+eng"
OCR_PORT = 5000

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/", methods=["GET"])
def index():
    return "Tesseract OCR сервер работает. Для распознавания используйте POST на /ocr"

@app.route("/ocr", methods=["POST"])
def ocr_file():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400

    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    ext = file.filename.lower().split('.')[-1]
    pages = []

    try:
        if ext == "pdf":
            images = convert_from_path(filepath)
            for img in images:
                img = img.convert("L")
                pages.append(img)
        else:
            img = Image.open(filepath)
            img = img.convert("L")
            pages.append(img)
    except Exception as e:
        return jsonify({"error": f"File conversion failed: {e}"}), 500

    all_text = []
    for img in pages:
        text = pytesseract.image_to_string(img, lang=OCR_LANG)
        all_text.append(text)

    csv_output = io.StringIO()
    writer = csv.writer(csv_output)
    for page_text in all_text:
        for line in page_text.splitlines():
            if line.strip():
                columns = [col.strip() for col in line.split('\t')]
                if len(columns) == 1:
                    columns = line.split()
                writer.writerow(columns)

    csv_output.seek(0)

    return send_file(
        io.BytesIO(csv_output.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name="output.csv"
    )

@app.route("/langs", methods=["GET"])
def langs():
    try:
        langs = pytesseract.get_languages()
        return "<pre>" + "\n".join(langs) + "</pre>"
    except Exception as e:
        return str(e)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=OCR_PORT)
