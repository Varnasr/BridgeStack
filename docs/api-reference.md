# API Reference

All endpoints are read-only (GET) and prefixed with `/api/v1`. The API returns JSON and follows RESTful conventions.

Interactive documentation is available at `/docs` (Swagger UI) and `/redoc` (ReDoc) when the server is running.

---

## Health

### `GET /`

Returns API metadata and the OpenStacks ecosystem map.

**Response:**
```json
{
  "name": "BridgeStack API",
  "version": "0.3.0",
  "docs": "/docs",
  "stacks": {
    "data": "RootStack",
    "api": "BridgeStack",
    "frontend": "ViewStack",
    "analysis": "EquityStack",
    "fieldwork": "FieldStack",
    "mel": "InsightStack",
    "content": "SignalStack"
  }
}
```

### `GET /health`

Returns health status including database connectivity.

**Response:**
```json
{
  "status": "healthy",
  "version": "0.3.0",
  "database": "connected"
}
```

Possible `status` values: `healthy`, `degraded`.

---

## Geography

### `GET /api/v1/geography/states`

List all states.

| Parameter | Type | Description |
|-----------|------|-------------|
| `region` | string | Filter by region (e.g. `South`, `West`, `North`, `East`, `Northeast`) |

**Example:** `GET /api/v1/geography/states?region=South`

### `GET /api/v1/geography/states/{state_id}`

Get a state with its districts.

**Response includes:** `state_id`, `state_name`, `region`, `state_type`, `capital`, `area_sq_km`, `census_2011_pop`, `districts[]`

### `GET /api/v1/geography/districts`

List all districts.

| Parameter | Type | Description |
|-----------|------|-------------|
| `state_id` | string | Filter by parent state |
| `tier` | string | Filter by tier (e.g. `Tier-1`, `Tier-2`, `Tier-3`) |

### `GET /api/v1/geography/districts/{district_id}`

Get a single district by ID.

---

## Sectors

### `GET /api/v1/sectors/`

List all development sectors. Sectors are hierarchical — child sectors have a `parent_id`.

### `GET /api/v1/sectors/{sector_id}`

Get a single sector by ID.

---

## Indicators

### `GET /api/v1/indicators/`

List indicators.

| Parameter | Type | Description |
|-----------|------|-------------|
| `sector_id` | string | Filter by sector |
| `source` | string | Filter by data source (partial match) |

### `GET /api/v1/indicators/{indicator_id}`

Get an indicator with all its data values.

**Response includes:** indicator metadata + `values[]` array with `state_id`, `year`, `value` entries.

### `GET /api/v1/indicators/values/`

Query indicator data points directly.

| Parameter | Type | Description |
|-----------|------|-------------|
| `indicator_id` | string | Filter by indicator |
| `state_id` | string | Filter by state |
| `year` | integer | Filter by year |

**Example:** `GET /api/v1/indicators/values/?indicator_id=IMR&state_id=KA&year=2020`

---

## Policies

### `GET /api/v1/policies/schemes`

List government schemes.

| Parameter | Type | Description |
|-----------|------|-------------|
| `sector_id` | string | Filter by sector |
| `status` | string | Filter by status (e.g. `Active`, `Closed`) |
| `level` | string | Filter by funding level (e.g. `Central`, `State`) |

### `GET /api/v1/policies/schemes/{scheme_id}`

Get a scheme with its budgets and coverage data.

**Response includes:** scheme metadata + `budgets[]` + `coverage[]`

### `GET /api/v1/policies/budgets`

Query scheme budget allocations.

| Parameter | Type | Description |
|-----------|------|-------------|
| `scheme_id` | string | Filter by scheme |
| `fiscal_year` | string | Filter by fiscal year (e.g. `2022-23`) |

### `GET /api/v1/policies/coverage`

Query scheme coverage (beneficiaries reached).

| Parameter | Type | Description |
|-----------|------|-------------|
| `scheme_id` | string | Filter by scheme |
| `state_id` | string | Filter by state |

---

## Tools

### `GET /api/v1/tools/`

List tools from the OpenStacks tool catalog.

| Parameter | Type | Description |
|-----------|------|-------------|
| `stack` | string | Filter by stack (e.g. `ViewStack`, `EquityStack`) |
| `language` | string | Filter by language (e.g. `Python`, `JavaScript`, `R`) |
| `tool_type` | string | Filter by type (e.g. `dashboard`, `notebook`, `script`) |
| `difficulty` | string | Filter by difficulty (`beginner`, `intermediate`, `advanced`) |

### `GET /api/v1/tools/{tool_id}`

Get a single tool by numeric ID.

---

## Error Responses

All endpoints return standard HTTP error codes:

| Code | Meaning |
|------|---------|
| `200` | Success |
| `404` | Resource not found |
| `422` | Validation error (invalid query parameters) |
| `500` | Internal server error |

Error response format:
```json
{
  "detail": "State not found"
}
```
