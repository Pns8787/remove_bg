FROM python:3.10-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Use explicit port 10000 in CMD (no variable)
CMD ["sh", "-c", "waitress-serve --port=10000 --host=0.0.0.0 app:app"]
