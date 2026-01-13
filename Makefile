.PHONY: install dev test lint format docker-build docker-run clean

install:
	uv sync

dev:
	uv run python -m server.main

test:
	uv run pytest

test-integration:
	@echo "Running integration tests..."
	uv run --env-file .env pytest tests/test_integration.py --run-integration

lint:
	uv run ruff check --fix src

format:
	uv run ruff format src

check:
	uv run ty check src

run-inspector:
	npx @modelcontextprotocol/inspector uv run ksc-mcp

docker-build:
	docker compose build

docker-run:
	docker compose up

clean:
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf __pycache__
