from flask import Flask, request, send_file, jsonify
import os, io, csv
from PIL import Image
import pytesseract
from pdf2image import convert_from_path

# Создаем Flask-приложение
app = Flask(__name__)

# Папка для сохранения загруженных файлов
UPLOAD_FOLDER = "uploads"
# Языки для Tesseract
OCR_LANG = "rus+kaz+eng"
# Создаем папку, если её нет
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# GET endpoint для проверки сервера
@app.route("/health", methods=["GET"])
def health():
    # Простой JSON, чтобы Render и пользователь понимали, что сервер жив
    return {"status": "ok"}

# POST endpoint для OCR и генерации CSV
@app.route("/ocr", methods=["POST"])
def ocr_file():
    # Проверка, что файл передан
    if "file" not in request.files:
        return "No file provided", 400

    # Сохраняем файл на сервер
    file = request.files["file"]
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)
    ext = file.filename.lower().split('.')[-1]

    # Массив страниц (для PDF может быть несколько)
    pages = []
    if ext == "pdf":
        # Конвертируем PDF в изображения
        images = convert_from_path(filepath)
        for img in images:
            pages.append(img.convert("L"))  # конвертируем в grayscale
    else:
        # Открываем обычное изображение
        img = Image.open(filepath)
        pages.append(img.convert("L"))

    # Генерация CSV
    csv_io = io.StringIO()
    writer = csv.writer(csv_io)
    for img in pages:
        # Распознаем текст через pytesseract
        text = pytesseract.image_to_string(img, lang=OCR_LANG)
        for line in text.splitlines():
            if line.strip():  # пропускаем пустые строки
                # Разбиваем по табуляции или пробелам
                columns = [col.strip() for col in line.split('\t')]
                if len(columns) == 1:
                    columns = line.split()
                writer.writerow(columns)

    csv_io.seek(0)
    # Отправляем CSV как файл
    return send_file(
        io.BytesIO(csv_io.getvalue().encode('utf-8')),
        mimetype='text/csv',
        as_attachment=True,
        download_name="output.csv"
    )

# POST endpoint для тестового OCR (только текст в JSON)
@app.route("/ocr_test", methods=["POST"])
def ocr_test():
    if "file" not in request.files:
        return jsonify({"error": "No file provided"}), 400
    file = request.files["file"]
    img = Image.open(file)
    text = pytesseract.image_to_string(img, lang=OCR_LANG)
    return jsonify({"text": text})

# Запуск сервера
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    # host="0.0.0.0" чтобы Docker/Render мог видеть сервер
    app.run(host="0.0.0.0", port=port)
