FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    && rm -rf /var/lib/apt/lists/*

# Server runtime only (no torch/chromadb — not needed for boot)
COPY requirements-server.txt .
RUN pip install --no-cache-dir -r requirements-server.txt

COPY . .

EXPOSE 8000

CMD ["uvicorn", "baton_server.main:app", "--host", "0.0.0.0", "--port", "8000"]
