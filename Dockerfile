# Базовый образ Ubuntu 22.04
FROM ubuntu:22.04

# Отключаем интерактивные вопросы при установке пакетов
ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow

# Устанавливаем системные зависимости и Tesseract с языками
RUN apt-get update && \
    apt-get install -y \
        tzdata \                # временная зона
        python3 \               # Python 3
        python3-pip \           # pip для Python 3
        python3-dev \           # заголовочные файлы Python
        tesseract-ocr \         # сам OCR движок
        tesseract-ocr-rus \     # русский язык
        tesseract-ocr-kaz \     # казахский язык
        tesseract-ocr-eng \     # английский язык
        libtesseract-dev \      # dev-библиотеки для Tesseract
        libleptonica-dev \      # библиотека обработки изображений
        poppler-utils \         # для конвертации PDF
        python3-pil \           # Pillow для Python
        python3-opencv \        # OpenCV
        curl \
        wget \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Рабочая папка
WORKDIR /app

# Копируем Python сервер в контейнер
COPY ocr_server.py /app

# Устанавливаем Python-библиотеки
RUN pip3 install --no-cache-dir flask pillow pytesseract pdf2image

# Папка для загрузки файлов
RUN mkdir -p /app/uploads

# Экспонируем порт для Render
EXPOSE 5000

# Запуск сервера
CMD ["python3", "ocr_server.py"]
