# Roadmap

This document outlines the planned future development for BridgeStack.

## v0.4 — Query Enhancements

- [ ] Pagination (`limit` / `offset` query params) for all list endpoints
- [ ] Rate limiting with configurable thresholds
- [ ] Response caching with `Cache-Control` / `ETag` headers
- [ ] Sorting support (`?sort=name`, `?order=desc`)

## v0.5 — Data & Search

- [ ] Full-text search across indicators and schemes
- [ ] Aggregation endpoints (state-level summaries, sector rollups)
- [ ] Bulk data export (CSV/JSON download)
- [ ] Cross-domain queries (indicators + schemes by state)

## v0.6 — Production Hardening

- [ ] PostgreSQL adapter (configurable via `DATABASE_URL`)
- [ ] Authentication for write operations (API key / OAuth2)
- [ ] Structured JSON logging for production monitoring
- [ ] OpenTelemetry tracing integration

## v0.7 — Real-Time & Integration

- [ ] WebSocket support for real-time data subscriptions
- [ ] Webhook notifications for data updates
- [ ] GraphQL endpoint alongside REST
- [ ] Multilingual response support

## Ongoing

- Expand and optimise schemas, queries, and API surface
- Improve documentation with visual diagrams and interactive tutorials
- Integrate broader OpenStacks ecosystem capabilities
- Community contributions and feedback incorporation

---

*This roadmap evolves as the project grows. Suggestions welcome via [GitHub Issues](https://github.com/Varnasr/BridgeStack/issues).*
