# Deployment

## Docker (Recommended)

### Quick Start

```bash
docker compose up --build -d
```

This builds the image and starts the API on port 8000.

### Docker Compose

```yaml
services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - ./rootstack.db:/app/rootstack.db
    environment:
      - BRIDGE_DATABASE_URL=sqlite:///./rootstack.db
      - BRIDGE_DEBUG=false
      - BRIDGE_LOG_LEVEL=INFO
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "python", "-c", "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')"]
      interval: 30s
      timeout: 5s
      retries: 3
```

### Building Manually

```bash
docker build -t bridgestack:latest .
docker run -p 8000:8000 -v ./rootstack.db:/app/rootstack.db bridgestack:latest
```

## Direct Deployment

### With Uvicorn

```bash
# Development
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Production (multiple workers)
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

### With Gunicorn + Uvicorn Workers

```bash
pip install gunicorn
gunicorn app.main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

## Health Monitoring

The `/health` endpoint checks database connectivity:

```bash
curl http://localhost:8000/health
```

**Healthy response:**
```json
{"status": "healthy", "version": "0.3.0", "database": "connected"}
```

**Degraded response** (database unreachable):
```json
{"status": "degraded", "version": "0.3.0", "database": "unavailable"}
```

Use this endpoint for container orchestration health checks (Docker, Kubernetes).

## Production Checklist

- [ ] Set `BRIDGE_DEBUG=false`
- [ ] Restrict `BRIDGE_CORS_ORIGINS` to known domains
- [ ] Set `BRIDGE_LOG_LEVEL=WARNING` or `INFO`
- [ ] Mount the RootStack database file as a volume
- [ ] Run behind a reverse proxy (nginx, Caddy) for HTTPS
- [ ] Set up log aggregation for structured logs
- [ ] Configure container health checks
