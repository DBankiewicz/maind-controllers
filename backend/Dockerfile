FROM python:3.11-slim

# Set a predictable app directory so the package `backend` is importable
WORKDIR /app

# Install build tools + SQLite dev
RUN apt-get update && apt-get install -y \
    gcc \
    make \
    build-essential \
    sqlite3 \
    libsqlite3-dev \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/backend/
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy the backend package sources into a `backend/` folder in the image so
# `import backend` works when Python's sys.path includes /app
COPY . /app/backend

# Ensure Python finds the package root (/app)
ENV PYTHONPATH=/app

# Default command - can be overridden by docker-compose for development
CMD ["uvicorn", "backend.main:app", "--host", "0.0.0.0", "--port", "8001", "--app-dir", "/app"]