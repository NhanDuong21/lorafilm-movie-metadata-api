.PHONY: setup test run lint format typecheck docker-build docker-run

setup:
	pip install -e ".[dev]"

test:
	pytest --cov=app --cov-report=term-missing

lint:
	ruff check .

format:
	ruff format .

typecheck:
	mypy app

run:
	uvicorn app.main:app --reload --port 8090

docker-build:
	docker build -t lorafilm-movie-metadata-api .

docker-run:
	docker compose up --build
