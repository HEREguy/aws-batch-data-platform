# Makefile for AWS ELT Portfolio Project
# Common commands for local development

.PHONY: help up down logs restart test-unit test-integration lint format clean

# Default target
help:
	@echo "AWS ELT Portfolio Project - Available commands:"
	@echo ""
	@echo "  make up              - Start all services (Airflow, Postgres)"
	@echo "  make down            - Stop all services"
	@echo "  make logs            - Follow logs from all services"
	@echo "  make restart         - Restart all services"
	@echo "  make test-unit       - Run unit tests"
	@echo "  make test-integration - Run integration tests (requires services running)"
	@echo "  make lint            - Run linters (ruff, mypy)"
	@echo "  make format          - Auto-format code with ruff"
	@echo "  make clean           - Remove containers, volumes, and virtual env"
	@echo "  make airflow-cli     - Run Airflow CLI command (usage: make airflow-cli CMD='dags list')"
	@echo "  make init-connections - Initialize Airflow connections from config"
	@echo ""

# Start all services
up:
	docker compose up -d
	@echo ""
	@echo "Services starting... Airflow UI will be available at http://localhost:8080"
	@echo "Username: admin | Password: admin"

# Stop all services
down:
	docker compose down

# Follow logs
logs:
	docker compose logs -f

# Restart services
restart:
	docker compose restart

# Run unit tests
test-unit:
	uv run pytest tests/unit -v --tb=short

# Run integration tests (requires services running)
test-integration:
	uv run pytest tests/integration -v --tb=short

# Run all tests
test: test-unit test-integration

# Lint code
lint:
	uv run ruff check .
	uv run mypy .

# Format code
format:
	uv run ruff check --fix .
	uv run ruff format .

# Clean everything
clean:
	docker compose down -v
	rm -rf .venv
	rm -rf __pycache__
	rm -rf .pytest_cache
	rm -rf .mypy_cache
	rm -rf .ruff_cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true

# Run Airflow CLI command
# Usage: make airflow-cli CMD="dags list"
airflow-cli:
	docker compose exec airflow-webserver airflow $(CMD)

# Initialize Airflow connections from config/connections.yaml
init-connections:
	docker compose exec airflow-webserver python /opt/airflow/scripts/init_connections.py

# Build custom Airflow image
build:
	docker compose build

# Show status of services
status:
	docker compose ps

# Open Airflow UI in browser (macOS)
open-ui:
	open http://localhost:8080