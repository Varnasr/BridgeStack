# Getting Started

## Prerequisites

- **Python 3.11+** (3.12 recommended)
- **Git**
- **RootStack database** (optional — the API works without data, but endpoints will return empty results)

## Installation

### From Source

```bash
# Clone the repository
git clone https://github.com/Varnasr/BridgeStack.git
cd BridgeStack

# Create a virtual environment
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### With Docker

```bash
docker compose up --build
```

The API will be available at `http://localhost:8000`.

## Running the API

```bash
uvicorn app.main:app --reload
```

Open [http://localhost:8000/docs](http://localhost:8000/docs) for the interactive Swagger UI.

## Your First Request

```bash
# Check API health
curl http://localhost:8000/health

# List all states
curl http://localhost:8000/api/v1/geography/states

# Filter states by region
curl "http://localhost:8000/api/v1/geography/states?region=South"

# Get indicator details
curl http://localhost:8000/api/v1/indicators/IMR
```

## Populating the Database

BridgeStack reads from a RootStack SQLite database. To populate it:

```bash
# Clone RootStack
git clone https://github.com/Varnasr/RootStack.git
cd RootStack
bash scripts/setup.sh

# Copy the database to BridgeStack
cp rootstack.db ../BridgeStack/
```

Then restart the API — all endpoints will return data.

## Development Setup

For contributors, install the dev tools:

```bash
pip install -e ".[dev]"

# Or use Make
make dev
```

This installs `ruff` (linter/formatter) and `pytest` with coverage support.

### Useful Make Commands

```bash
make test      # Run tests with coverage
make lint      # Check for lint issues
make format    # Auto-format code
make check     # Run all checks (lint + test)
make run       # Start dev server
```

## Next Steps

- [API Reference](api-reference.md) — Explore all available endpoints
- [Configuration](configuration.md) — Customize BridgeStack settings
- [Architecture](architecture.md) — Understand the system design
