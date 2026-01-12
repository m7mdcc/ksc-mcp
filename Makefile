.PHONY: install dev test lint format docker-build docker-run clean

install:
	uv sync

dev:
	uv run python -m src.server.main

test:
	uv run pytest

lint:
	uv run ruff check --fix src

format:
	uv run ruff format src

docker-build:
	docker compose build

docker-run:
	docker compose up

clean:
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf .ruff_cache
	rm -rf __pycache__
