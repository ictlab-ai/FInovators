FROM ubuntu:22.04

# Системные зависимости
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

WORKDIR /app

# Копируем Python-приложение
COPY ocr_server.py /app

# Python-библиотеки
RUN pip3 install --no-cache-dir flask pillow

# Папка для загруженных файлов
RUN mkdir -p /app/uploads

EXPOSE 5000

CMD ["python3", "ocr_server.py"]
