# Makefile for Autonomous User Interface Engine
# Phase 1: Quick Wins & Foundation

.PHONY: help install install-dev format lint test test-cov clean pre-commit-install pre-commit-run

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
