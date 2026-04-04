# Architecture

## System Overview

BridgeStack is the API middleware in the OpenStacks ecosystem. It reads from a RootStack SQLite database and exposes RESTful endpoints consumed by multiple frontend and analysis Stacks.

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────────────────┐
│  RootStack   │────▶│ BridgeStack  │────▶│  Consumer Stacks            │
│  (SQLite DB) │     │  (FastAPI)   │     │                             │
│              │     │              │     │  ViewStack    (dashboards)   │
│  - States    │     │  /api/v1/    │     │  EquityStack  (analysis)    │
│  - Districts │     │              │     │  FieldStack   (fieldwork)   │
│  - Sectors   │     │  GET-only    │     │  InsightStack (MEL)         │
│  - Indicators│     │  JSON API    │     │  SignalStack  (content)     │
│  - Schemes   │     │              │     │                             │
│  - Tools     │     │              │     │                             │
└─────────────┘     └──────────────┘     └─────────────────────────────┘
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| Framework | FastAPI 0.115+ | Async-capable REST framework with auto-generated OpenAPI docs |
| ORM | SQLAlchemy 2.0+ | Database abstraction with relationship mapping |
| Validation | Pydantic 2.11+ | Request/response schema validation |
| Database | SQLite | Lightweight, file-based storage (PostgreSQL planned) |
| Server | Uvicorn 0.34+ | ASGI server for production and development |

## Application Structure

```
app/
├── main.py              # FastAPI app, middleware, health endpoints
├── core/
│   ├── config.py        # Pydantic settings (env-configurable)
│   └── database.py      # Engine, session factory, dependency injection
├── models/              # SQLAlchemy ORM models (5 domains)
│   ├── geography.py     # State, District
│   ├── sectors.py       # Sector (hierarchical)
│   ├── indicators.py    # Indicator, IndicatorValue
│   ├── policies.py      # Scheme, SchemeBudget, SchemeCoverage
│   └── tools.py         # Tool
├── schemas/             # Pydantic response models
│   ├── geography.py     # StateBase, StateDetail, DistrictBase
│   ├── sectors.py       # SectorBase, SectorTree
│   ├── indicators.py    # IndicatorBase, IndicatorDetail, IndicatorValueBase
│   ├── policies.py      # SchemeBase, SchemeDetail, SchemeBudgetBase, SchemeCoverageBase
│   └── tools.py         # ToolBase
└── routes/              # API endpoint handlers
    ├── geography.py     # 4 endpoints
    ├── sectors.py       # 2 endpoints
    ├── indicators.py    # 3 endpoints
    ├── policies.py      # 4 endpoints
    └── tools.py         # 2 endpoints
```

## Data Model

### Entity Relationships

```
sectors ◄──────────── indicators ──────────► indicator_values
   ▲                                              │
   │                                              │
   └── schemes ──┬── scheme_budgets         states ◄──── districts
                 └── scheme_coverage ────────►│
```

### Key Design Decisions

1. **Read-only API**: BridgeStack exposes only GET endpoints. Data is managed through RootStack.

2. **Eager loading**: Detail endpoints use `joinedload()` to fetch related records in a single query, avoiding N+1 problems.

3. **SQLite foreign keys**: Explicitly enabled via SQLAlchemy event listener (`PRAGMA foreign_keys=ON`) since SQLite disables them by default.

4. **Dependency injection**: Database sessions are managed through FastAPI's `Depends(get_db)` pattern, ensuring proper cleanup.

5. **Schema separation**: SQLAlchemy models (database) and Pydantic schemas (API) are kept separate, allowing the API contract to evolve independently of the database schema.

## Request Flow

```
HTTP Request
    │
    ▼
FastAPI Router (routes/*.py)
    │
    ├── Query parameter validation (Pydantic)
    ├── Database session injection (Depends)
    │
    ▼
SQLAlchemy Query (models/*.py)
    │
    ├── Filters applied from query params
    ├── Eager loading for detail endpoints
    │
    ▼
Pydantic Serialization (schemas/*.py)
    │
    ▼
JSON Response
```
