FROM ubuntu:22.04

ENV DEBIAN_FRONTEND=noninteractive
ENV TZ=Europe/Moscow

# Системные зависимости + Tesseract
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

WORKDIR /app

COPY ocr_server.py /app

RUN pip3 install --no-cache-dir flask pillow pytesseract pdf2image

RUN mkdir -p /app/uploads

EXPOSE 5000

CMD ["python3", "ocr_server.py"]
