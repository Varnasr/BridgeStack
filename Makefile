.PHONY: install dev test lint format run docker-up docker-down clean

install:  ## Install production dependencies
	pip install -r requirements.txt

dev:  ## Install all dependencies (including dev tools)
	pip install -e ".[dev]"

test:  ## Run tests with coverage
	pytest --cov=app --cov-report=term-missing

lint:  ## Run linter
	ruff check .

format:  ## Format code
	ruff format .
	ruff check --fix .

check:  ## Run all checks (lint + test)
	ruff format --check .
	ruff check .
	pytest --cov=app

run:  ## Start the development server
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

docker-up:  ## Start with Docker Compose
	docker compose up --build -d

docker-down:  ## Stop Docker Compose
	docker compose down

clean:  ## Remove build artifacts and caches
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -exec rm -rf {} + 2>/dev/null || true
	rm -f .coverage coverage.xml
	rm -f test.db

help:  ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-15s\033[0m %s\n", $$1, $$2}'
