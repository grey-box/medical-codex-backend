# syntax=docker/dockerfile:1

# Use a slim Python 3.10 image
FROM python:3.10-slim

# Label for authorship
LABEL authors="Grey-Box, François Pelletier"

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    gfortran \
    pkg-config \
    libopenblas-dev \
    liblapack-dev \
    libpq-dev \
    curl \
    wget \
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    git \
    python3-dev \
    ninja-build \
    ffmpeg \
    clamav \
    clamav-daemon \
    clamav-freshclam \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*



#Update ClamAv database
RUN freshclam

# ──────────────────────────────────────────────
# Configure ClamAV to use TCP, not Unix socket
# ──────────────────────────────────────────────
RUN echo "\
LogSyslog yes\n\
LogFile /var/log/clamav/clamd.log\n\
TCPSocket 3310\n\
TCPAddr 127.0.0.1\n\
Foreground yes\n\
FixStaleSocket yes\n\
MaxConnectionQueueLength 30\n\
ScanPE yes\n\
ScanELF yes\n\
ScanOLE2 yes\n\
ScanPDF yes\n\
ScanHTML yes\n\
DetectPUA yes\n\
ExitOnOOM yes\n" > /etc/clamav/clamd.conf


# Set working directory
WORKDIR /app

# Upgrade pip and install Python build tools
RUN pip install --upgrade pip setuptools wheel meson ninja pythran==0.12.2

# Copy only requirements first (leverage Docker cache)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --prefer-binary -r requirements.txt

# ──────────────────────────────────────────────
# Pre-download PaddleOCR Models
# ──────────────────────────────────────────────
ENV PADDLEOCR_HOME=/root/.paddleocr/whl
RUN mkdir -p $PADDLEOCR_HOME/det/en/en_PP-OCRv3_det_infer \
    $PADDLEOCR_HOME/rec/en/en_PP-OCRv3_rec_infer \
    $PADDLEOCR_HOME/cls/ch_ppocr_mobile_v2.0_cls_infer && \
    wget -O /tmp/en_PP-OCRv3_det_infer.tar \
    https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_det_infer.tar && \
    tar --strip-components=1 -xvf /tmp/en_PP-OCRv3_det_infer.tar \
    -C $PADDLEOCR_HOME/det/en/en_PP-OCRv3_det_infer && rm /tmp/en_PP-OCRv3_det_infer.tar && \
    wget -O /tmp/en_PP-OCRv3_rec_infer.tar \
    https://paddleocr.bj.bcebos.com/PP-OCRv3/english/en_PP-OCRv3_rec_infer.tar && \
    tar --strip-components=1 -xvf /tmp/en_PP-OCRv3_rec_infer.tar \
    -C $PADDLEOCR_HOME/rec/en/en_PP-OCRv3_rec_infer && rm /tmp/en_PP-OCRv3_rec_infer.tar && \
    wget -O /tmp/ch_ppocr_mobile_v2.0_cls_infer.tar \
    https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar && \
    tar --strip-components=1 -xvf /tmp/ch_ppocr_mobile_v2.0_cls_infer.tar \
    -C $PADDLEOCR_HOME/cls/ch_ppocr_mobile_v2.0_cls_infer && rm /tmp/ch_ppocr_mobile_v2.0_cls_infer.tar

ENV \
    DET_MODEL_DIR=$PADDLEOCR_HOME/det/en/en_PP-OCRv3_det_infer \
    REC_MODEL_DIR=$PADDLEOCR_HOME/rec/en/en_PP-OCRv3_rec_infer \
    CLS_MODEL_DIR=$PADDLEOCR_HOME/cls/ch_ppocr_mobile_v2.0_cls_infer

# ──────────────────────────────────────────────

# Copy the actual app code
COPY ./app/ .

# Expose FastAPI app port
EXPOSE 8080

# Start ClamAV + wait for readiness + run FastAPI
CMD sh -c '\
    clamd & \
    echo "Waiting for ClamAV to start..." && \
    for i in $(seq 1 10); do \
        nc -z 127.0.0.1 3310 && break || sleep 1; \
    done && \
    echo "ClamAV ready. Starting FastAPI." && \
    uvicorn main:app --host 0.0.0.0 --port 8080 $UVICORN_RELOAD'