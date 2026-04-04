# BridgeStack

**API backend bridging OpenStacks data layers.**

[![CI](https://github.com/Varnasr/BridgeStack/actions/workflows/ci.yml/badge.svg)](https://github.com/Varnasr/BridgeStack/actions/workflows/ci.yml)
[![Part of OpenStacks](https://img.shields.io/badge/Part%20of-OpenStacks-blue)](https://openstacks.dev)
[![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)
[![Python 3.11+](https://img.shields.io/badge/Python-3.11%2B-blue)]()
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-009688)]()
[![Code style: Ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://docs.astral.sh/ruff/)

> The API layer for [OpenStacks](https://openstacks.dev) — connecting database to frontend.

---

## Quick Start

```bash
git clone https://github.com/Varnasr/BridgeStack.git
cd BridgeStack
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) for interactive API docs.

### With Docker

```bash
docker compose up --build
```

### With Make

```bash
make dev       # install with dev tools
make run       # start the server
make test      # run tests with coverage
make check     # lint + test
```

## Architecture

```
RootStack (SQLite) → BridgeStack (FastAPI) → ViewStack / EquityStack / FieldStack
```

BridgeStack serves as the middleware connecting [RootStack](https://github.com/Varnasr/RootStack) data to all consumer Stacks:

| Stack | Role | Connection |
|-------|------|------------|
| [RootStack](https://github.com/Varnasr/RootStack) | SQLite schemas & seed data | Data source |
| **BridgeStack** (this repo) | REST API (FastAPI) | You are here |
| [ViewStack](https://github.com/Varnasr/ViewStack) | Frontend dashboards | Consumes API |
| [EquityStack](https://github.com/Varnasr/EquityStack) | Python analysis workflows | Consumes API |
| [FieldStack](https://github.com/Varnasr/FieldStack) | R fieldwork tools | Consumes API |
| [InsightStack](https://github.com/Varnasr/InsightStack) | MEL tools | Consumes API |
| [SignalStack](https://github.com/Varnasr/SignalStack) | Curated content | Consumes API |

## API Endpoints

All endpoints are prefixed with `/api/v1`. Full reference: [docs/api-reference.md](docs/api-reference.md)

| Domain | Endpoints | Filters |
|--------|-----------|---------|
| **Geography** | `states`, `districts` | `region`, `state_id`, `tier` |
| **Sectors** | `sectors` | — |
| **Indicators** | `indicators`, `values` | `sector_id`, `source`, `state_id`, `year` |
| **Policies** | `schemes`, `budgets`, `coverage` | `sector_id`, `status`, `level`, `fiscal_year` |
| **Tools** | `tools` | `stack`, `language`, `tool_type`, `difficulty` |
| **Health** | `/`, `/health` | — |

## Documentation

Full documentation is in the [`docs/`](docs/) directory:

- [Getting Started](docs/getting-started.md) — Installation and first request
- [API Reference](docs/api-reference.md) — Complete endpoint docs
- [Architecture](docs/architecture.md) — System design and data model
- [Configuration](docs/configuration.md) — Environment variables
- [Deployment](docs/deployment.md) — Docker, production, monitoring

## Configuration

Environment variables (prefix `BRIDGE_`):

| Variable | Default | Description |
|----------|---------|-------------|
| `BRIDGE_DATABASE_URL` | `sqlite:///./rootstack.db` | Database connection string |
| `BRIDGE_DEBUG` | `false` | Enable debug mode |
| `BRIDGE_CORS_ORIGINS` | `["*"]` | Allowed CORS origins |
| `BRIDGE_LOG_LEVEL` | `INFO` | Logging level |

See [.env.example](.env.example) for a starter configuration.

## Development

```bash
# Install dev dependencies
pip install -e ".[dev]"

# Run tests
pytest --cov=app

# Lint & format
ruff check .
ruff format .
```

## Project Structure

```
BridgeStack/
├── app/
│   ├── main.py              # FastAPI app entry point
│   ├── core/
│   │   ├── config.py        # Settings (env-configurable)
│   │   └── database.py      # SQLAlchemy setup
│   ├── models/              # SQLAlchemy ORM models
│   ├── schemas/             # Pydantic response schemas
│   └── routes/              # API route handlers
├── tests/                   # Pytest test suite
├── docs/                    # Project documentation
├── pyproject.toml           # Project metadata & tool config
├── requirements.txt         # Python dependencies
├── Makefile                 # Development commands
├── Dockerfile               # Container image
└── docker-compose.yml       # Local orchestration
```

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines. Areas where contributions are welcome:

- Additional query endpoints and aggregations
- Pagination and rate limiting
- Response caching
- PostgreSQL adapter
- WebSocket support for real-time data

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before participating.

## License

MIT — free to use, modify, and share. See [LICENSE](LICENSE).

---

**Created by [Varna Sri Raman](https://github.com/Varnasr)** — Development Economist & Social Researcher

Part of the [OpenStacks](https://openstacks.dev) ecosystem by [ImpactMojo](https://impactmojo.in).
