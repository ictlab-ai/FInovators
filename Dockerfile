FROM ubuntu:22.04

# Системные зависимости и Tesseract
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        python3-dev \
        tesseract-ocr \
        tesseract-ocr-rus \
        tesseract-ocr-kaz \
        tesseract-ocr-eng \
        libtesseract-dev \
        libleptonica-dev \
        poppler-utils \
        python3-pil \
        python3-opencv \
        curl \
        wget \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Копируем Python-приложение
COPY ocr_server.py /app

# Python-библиотеки
RUN pip3 install --no-cache-dir flask pillow pytesseract pdf2image

# Папка для загруженных файлов
RUN mkdir -p /app/uploads

EXPOSE 5000

CMD ["python3", "ocr_server.py"]
