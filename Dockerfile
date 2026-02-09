# Base image: Python 3.10 slim
FROM python:3.10-slim

# Set working directory inside container
WORKDIR /app

# Install system dependencies (for pandas/pyarrow)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        build-essential \
        libpq-dev \
        && rm -rf /var/lib/apt/lists/*

# Copy Python requirements and install
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files into container
COPY . .

# Environment variable to avoid Python buffering (useful for logs)
ENV PYTHONUNBUFFERED=1

# Default command: run training
CMD ["python", "src/train.py"]
