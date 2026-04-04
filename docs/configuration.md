# Configuration

BridgeStack is configured through environment variables. All variables use the `BRIDGE_` prefix to avoid conflicts with other applications.

## Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `BRIDGE_DATABASE_URL` | `sqlite:///./rootstack.db` | Database connection string |
| `BRIDGE_DEBUG` | `false` | Enable debug mode (verbose errors) |
| `BRIDGE_CORS_ORIGINS` | `["*"]` | JSON array of allowed CORS origins |
| `BRIDGE_LOG_LEVEL` | `INFO` | Logging level (`DEBUG`, `INFO`, `WARNING`, `ERROR`) |

## Setup

Copy the example environment file and modify as needed:

```bash
cp .env.example .env
```

## Configuration Examples

### Development

```env
BRIDGE_DATABASE_URL=sqlite:///./rootstack.db
BRIDGE_DEBUG=true
BRIDGE_CORS_ORIGINS=["*"]
BRIDGE_LOG_LEVEL=DEBUG
```

### Production

```env
BRIDGE_DATABASE_URL=sqlite:///./data/rootstack.db
BRIDGE_DEBUG=false
BRIDGE_CORS_ORIGINS=["https://yourdomain.com","https://app.yourdomain.com"]
BRIDGE_LOG_LEVEL=WARNING
```

### Docker

Environment variables are set in `docker-compose.yml`:

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
```

## CORS Configuration

By default, CORS allows all origins (`["*"]`). For production, restrict this to known consumer applications:

```env
BRIDGE_CORS_ORIGINS=["https://viewstack.openstacks.dev","https://equitystack.openstacks.dev"]
```

## Database

BridgeStack currently supports **SQLite** as its database backend. The database file is created by [RootStack](https://github.com/Varnasr/RootStack) and contains all seed data.

PostgreSQL support is planned — see the [Roadmap](../ROADMAP.md).
