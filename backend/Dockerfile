FROM python:3.11-slim

WORKDIR /backend

# Install build tools + SQLite dev
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    build-essential \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8001"]