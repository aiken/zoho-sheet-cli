# Makefile for Zoho Sheet CLI

.PHONY: help install install-dev test test-cov lint format clean build upload

help:
	@echo "Zoho Sheet CLI - Available commands:"
	@echo ""
	@echo "  make install      - Install package"
	@echo "  make install-dev  - Install with development dependencies"
	@echo "  make test         - Run tests"
	@echo "  make test-cov     - Run tests with coverage"
	@echo "  make lint         - Run linting (black, flake8, mypy)"
	@echo "  make format       - Format code with black"
	@echo "  make clean        - Clean build artifacts"
	@echo "  make build        - Build distribution packages"
	@echo "  make upload       - Upload to PyPI"
	@echo "  make demo         - Run demo script"
	@echo ""

install:
	pip install -e .

install-dev:
	pip install -e ".[dev]"

test:
	pytest -v

test-cov:
	pytest -v --cov=zoho_sheet_cli --cov-report=html --cov-report=term

lint:
	black --check zoho_sheet_cli tests
	flake8 zoho_sheet_cli tests --max-line-length=88 --extend-ignore=E203
	mypy zoho_sheet_cli

format:
	black zoho_sheet_cli tests

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	rm -rf htmlcov/
	rm -rf .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete

build: clean
	python -m build

upload: build
	twine upload dist/*

demo:
	python examples/demo.py

# Quick test commands
test-auth:
	zsheet auth status

test-cli:
	zsheet --version
	zsheet --help
	zsheet workbook --help
	zsheet worksheet --help
	zsheet cell --help
	zsheet file --help
