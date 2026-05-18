# Deployment Guide

## Local Development

```bash
./install.sh
./run.sh
```

Open http://localhost:8000

## Docker

```bash
docker compose up -d
```

Open http://localhost:8000

## Docker (Production — without volume mount)

```bash
docker build -t baton:latest .
docker run -d --name baton -p 8000:8000 --restart unless-stopped baton:latest
```

## Docker with Ollama

If Ollama runs on the host machine:

```bash
# Linux
docker run -d --name baton -p 8000:8000 \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  baton:latest

# macOS/Windows (Docker Desktop)
docker run -d --name baton -p 8000:8000 \
  -e OLLAMA_HOST=http://host.docker.internal:11434 \
  baton:latest
```

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `SERVER_HOST` | `0.0.0.0` | Server bind address |
| `SERVER_PORT` | `8000` | Server port |
| `OLLAMA_HOST` | `http://host.docker.internal:11434` | Ollama endpoint |
| `CHROMA_DB_PATH` | `./baton_memory` | ChromaDB storage path |

## Health Checks

```bash
# API health
curl -f http://localhost:8000/api/status

# Metrics
curl -f http://localhost:8000/api/metrics

# UI
curl -f http://localhost:8000/
```

## Reverse Proxy (Nginx)

```nginx
server {
    listen 80;
    server_name baton.example.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

## System Requirements

- Python 3.11+
- 512MB RAM minimum (server only)
- 2GB RAM recommended (with ML stack)
- 1GB disk space
- Docker 20+ (optional)
