# Contributing to BridgeStack

Thank you for your interest in contributing to BridgeStack! This project is part of the [OpenStacks](https://openstacks.dev) ecosystem, and we welcome contributions of all kinds.

## Getting Started

### Prerequisites

- Python 3.11+
- Git

### Setup

```bash
git clone https://github.com/Varnasr/BridgeStack.git
cd BridgeStack
python -m venv .venv
source .venv/bin/activate   # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### Running Locally

```bash
uvicorn app.main:app --reload
```

API docs will be at [http://localhost:8000/docs](http://localhost:8000/docs).

### Running Tests

```bash
pytest                         # run all tests
pytest --cov=app               # with coverage
pytest -k "test_geography"     # run specific test class
```

### Linting & Formatting

```bash
ruff check .          # check for lint issues
ruff check --fix .    # auto-fix lint issues
ruff format .         # format code
```

## How to Contribute

### Reporting Bugs

Open an issue using the [bug report template](https://github.com/Varnasr/BridgeStack/issues/new?template=bug_report.md). Include:

- Steps to reproduce
- Expected vs actual behaviour
- Python version and OS

### Suggesting Features

Open an issue using the [feature request template](https://github.com/Varnasr/BridgeStack/issues/new?template=feature_request.md).

### Submitting Code

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/your-feature`
3. Make your changes
4. Run tests and linting:
   ```bash
   pytest --cov=app
   ruff check .
   ruff format --check .
   ```
5. Commit using the [commit conventions](#commit-conventions)
6. Push and open a pull request

### Commit Conventions

All commit messages must start with one of these prefixes:

| Prefix | Use for |
|--------|---------|
| `Add:` | New features or files |
| `Fix:` | Bug fixes |
| `Update:` | Enhancements to existing features |
| `Docs:` | Documentation changes |
| `Refactor:` | Code restructuring (no behaviour change) |
| `Test:` | Adding or updating tests |
| `CI:` | CI/CD pipeline changes |
| `Chore:` | Maintenance tasks |

Example: `Add: pagination support for indicator values endpoint`

### Pull Request Guidelines

- Keep PRs focused — one feature or fix per PR
- Include tests for new functionality
- Update documentation if you change API behaviour
- Fill in the PR template completely

## Project Structure

```
app/
├── core/          # Config, database setup, shared utilities
├── models/        # SQLAlchemy ORM models
├── schemas/       # Pydantic request/response schemas
└── routes/        # FastAPI route handlers
tests/             # Pytest test suite
docs/              # Project documentation
```

## Areas Where Help Is Welcome

- Additional query endpoints and aggregations
- Pagination and rate limiting
- Response caching
- PostgreSQL adapter
- Test coverage improvements
- Documentation and examples

## Code of Conduct

Please read our [Code of Conduct](CODE_OF_CONDUCT.md) before contributing.

## Questions?

Open a [discussion](https://github.com/Varnasr/BridgeStack/issues) or reach out at hello@impactmojo.in.
