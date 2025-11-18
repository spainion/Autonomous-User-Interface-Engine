# Makefile for Autonomous User Interface Engine
# Phase 1: Quick Wins & Foundation

.PHONY: help install install-dev format lint test test-cov clean pre-commit-install pre-commit-run docker-build docker-up docker-down docker-logs api-dev

help:  ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Available targets:'
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:  ## Install production dependencies
	pip install -r requirements.txt

install-dev:  ## Install development dependencies
	pip install -r requirements.txt
	pip install -r requirements-dev.txt

format:  ## Format code with Black and isort
	black .
	isort .

lint:  ## Run all linters
	@echo "Running Black..."
	black --check .
	@echo "Running isort..."
	isort --check-only .
	@echo "Running Flake8..."
	flake8 . --count --select=E9,F63,F7,F82 --show-source --statistics
	@echo "Running Pylint..."
	pylint **/*.py --max-line-length=120 || true
	@echo "Running mypy..."
	mypy . --ignore-missing-imports || true

test:  ## Run tests
	pytest tests/ -v

test-cov:  ## Run tests with coverage
	pytest tests/ --cov=. --cov-report=html --cov-report=term-missing -v

test-watch:  ## Run tests in watch mode (requires pytest-watch)
	ptw -- tests/ -v

clean:  ## Clean build artifacts and cache
	find . -type d -name "__pycache__" -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} + 2>/dev/null || true
	rm -rf .pytest_cache .mypy_cache .coverage htmlcov dist build

pre-commit-install:  ## Install pre-commit hooks
	pre-commit install

pre-commit-run:  ## Run pre-commit hooks on all files
	pre-commit run --all-files

security:  ## Run security checks
	@echo "Running Bandit..."
	bandit -r . -f json -o bandit-report.json || true
	@echo "Running Safety..."
	safety check || true

all: format lint test  ## Run format, lint, and test

ci: lint test security  ## Run CI pipeline locally

# Phase 2: Production Deployment Commands

docker-build:  ## Build Docker image
	docker build -t ui-engine:latest .

docker-up:  ## Start all services with docker-compose
	docker-compose up -d

docker-down:  ## Stop all services
	docker-compose down

docker-logs:  ## View docker-compose logs
	docker-compose logs -f

docker-restart:  ## Restart all services
	docker-compose restart

docker-clean:  ## Remove containers and volumes
	docker-compose down -v

api-dev:  ## Run API server in development mode
	python -m uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

api-prod:  ## Run API server in production mode
	python -m uvicorn api.main:app --host 0.0.0.0 --port 8000 --workers 4

# Phase 3: Quality & Security Commands

test-e2e:  ## Run end-to-end tests
	pytest tests/e2e/ -v -m e2e

test-performance:  ## Run performance tests
	pytest tests/performance/ -v -m performance

test-property:  ## Run property-based tests
	pytest tests/property/ -v -m property

test-all:  ## Run all tests including E2E
	pytest tests/ -v

load-test:  ## Run load tests with Locust
	locust -f locustfile.py --host=http://localhost:8000

security-scan:  ## Run comprehensive security scans
	@echo "Running Bandit..."
	bandit -r . -ll || true
	@echo "Running Safety..."
	safety check || true

coverage:  ## Generate and view coverage report
	pytest tests/ --cov=. --cov-report=html --cov-report=term-missing
	@echo "Coverage report generated in htmlcov/"

# Phase 4: Performance Optimization Commands

benchmark:  ## Run performance benchmarks
	@echo "Running performance benchmarks..."
	python -m benchmarks.bench_context_engine || true
	python -m benchmarks.bench_api || true

screenshots:  ## Capture screenshots with Playwright
	python screenshot_utility.py

visual-tests:  ## Run visual regression tests
	pytest tests/e2e/test_visual_regression.py -v

benchmark-all:  ## Run all benchmarks and generate report
	make benchmark
	@echo "Benchmarks complete!"

performance:  ## Run full performance test suite
	make benchmark
	make load-test
	make screenshots
