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
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

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

RUN mkdir -p /root/.paddleocr/whl/det/ch/ch_PP-OCRv3_det_infer \
    /root/.paddleocr/whl/rec/ch/ch_PP-OCRv3_rec_infer \
    /root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer && \
    wget -O /tmp/ch_PP-OCRv3_det_infer.tar \
    https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_det_infer.tar && \
    tar --strip-components=1 -xvf /tmp/ch_PP-OCRv3_det_infer.tar -C /root/.paddleocr/whl/det/ch/ch_PP-OCRv3_det_infer && \
    rm /tmp/ch_PP-OCRv3_det_infer.tar && \
    wget -O /tmp/ch_PP-OCRv3_rec_infer.tar \
    https://paddleocr.bj.bcebos.com/PP-OCRv3/chinese/ch_PP-OCRv3_rec_infer.tar && \
    tar --strip-components=1 -xvf /tmp/ch_PP-OCRv3_rec_infer.tar -C /root/.paddleocr/whl/rec/ch/ch_PP-OCRv3_rec_infer && \
    rm /tmp/ch_PP-OCRv3_rec_infer.tar && \
    wget -O /tmp/ch_ppocr_mobile_v2.0_cls_infer.tar \
    https://paddleocr.bj.bcebos.com/dygraph_v2.0/ch/ch_ppocr_mobile_v2.0_cls_infer.tar && \
    tar --strip-components=1 -xvf /tmp/ch_ppocr_mobile_v2.0_cls_infer.tar -C /root/.paddleocr/whl/cls/ch_ppocr_mobile_v2.0_cls_infer && \
    rm /tmp/ch_ppocr_mobile_v2.0_cls_infer.tar

# ──────────────────────────────────────────────

# Copy the actual app code
COPY ./app/ .

# Expose FastAPI app port
EXPOSE 8080

# Run app
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8080 $UVICORN_RELOAD"]
