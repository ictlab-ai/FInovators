from flask import Flask, request, send_file
import os, io, csv
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
OCR_LANG = "rus+kaz+eng"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/ocr", methods=["POST"])
def ocr_file():
    if "file" not in request.files:
        return "No file provided", 400

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

    # Генерация CSV
    csv_io = io.StringIO()
    writer = csv.writer(csv_io)
    for img in pages:
        text = pytesseract.image_to_string(img, lang=OCR_LANG)
        for line in text.splitlines():
            if line.strip():
                # Разделяем колонки по табуляции или пробелам
                columns = [col.strip() for col in line.split('\t')]
                if len(columns) == 1:
                    columns = line.split()
                writer.writerow(columns)

    csv_io.seek(0)
    return send_file(
        io.BytesIO(csv_io.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name="output.csv"
    )

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
