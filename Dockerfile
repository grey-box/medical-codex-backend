# syntax=docker/dockerfile:1

# Use a slim Python 3.11 image
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
    libgl1 \
    libglib2.0-0 \
    libsm6 \
    libxrender1 \
    libxext6 \
    git \
    python3-dev \
    ninja-build \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Upgrade pip and related tools
RUN pip install --upgrade pip setuptools wheel meson ninja pythran==0.12.2

# Copy only requirements first to use Docker cache
COPY requirements.txt .

# Install Python dependencies
RUN pip install --prefer-binary -r requirements.txt

# Copy the application source code
COPY ./app/ .

# Expose the application port
EXPOSE 8080

# Run the app
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8080 $UVICORN_RELOAD"]