# Используем базовый образ Ubuntu 22.04
FROM ubuntu:22.04

# --- Устанавливаем системные зависимости ---
RUN apt-get update && \
    apt-get install -y \
        python3 \
        python3-pip \
        python3-dev \
        curl \
        wget \
        cuneiform \
        libjpeg-dev \
        libtiff5-dev \
        zlib1g-dev \
        && apt-get clean \
        && rm -rf /var/lib/apt/lists/*

# --- Рабочая директория ---
WORKDIR /app

# --- Копируем Python-приложение ---
COPY ocr_server.py /app

# --- Устанавливаем Python-библиотеки ---
RUN pip3 install --no-cache-dir flask pillow

# --- Создаём папку для загрузок ---
RUN mkdir -p /app/uploads

# --- Открываем порт Flask ---
EXPOSE 5000

# --- Запуск приложения ---
CMD ["python3", "ocr_server.py"]
