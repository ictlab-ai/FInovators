FROM ubuntu:22.04

# Отключаем интерактивные вопросы при установке
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow

# Системные зависимости и Tesseract с языками
RUN apt-get update && \
    apt-get install -y \
        tzdata \
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

# Рабочая папка
WORKDIR /app

# Копируем Python-приложение
COPY ocr_server.py /app

# Устанавливаем Python-библиотеки
RUN pip3 install --no-cache-dir flask pillow pytesseract pdf2image

# Папка для загруженных файлов
RUN mkdir -p /app/uploads

# Экспонируем порт Render
EXPOSE 5000

# Запуск сервера напрямую через Python
CMD ["python3", "ocr_server.py"]
