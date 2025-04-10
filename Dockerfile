FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    wget \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Download model before installing Python dependencies
RUN mkdir -p /root/.u2net && \
    wget https://github.com/danielgatis/rembg/releases/download/v0.0.0/u2net.onnx -O /root/.u2net/u2net.onnx

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["sh", "-c", "waitress-serve --port=8080 --host=0.0.0.0 app:app"]
