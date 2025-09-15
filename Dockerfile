FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive

# Устанавливаем Cuneiform, ImageMagick и Python
RUN apt-get update && \
    apt-get install -y \
        cuneiform \
        imagemagick \
        python3 \
        python3-pip \
        python3-dev \
        curl \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ocr_server.py /app
RUN pip3 install flask

# Создаём папку для загрузки файлов
RUN mkdir -p /app/uploads

EXPOSE 5000
CMD ["python3", "ocr_server.py"]
