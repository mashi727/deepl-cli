.PHONY: help install install-dev test test-cov lint format type-check security clean build publish docs

PYTHON := python3
PIP := $(PYTHON) -m pip
PYTEST := $(PYTHON) -m pytest
BLACK := $(PYTHON) -m black
FLAKE8 := $(PYTHON) -m flake8
MYPY := $(PYTHON) -m mypy
BANDIT := $(PYTHON) -m bandit
SAFETY := $(PYTHON) -m safety

# Default target
help:
	@echo "DeepL CLI Development Commands"
	@echo "=============================="
	@echo "install        Install package in production mode"
	@echo "install-dev    Install package in development mode with all dependencies"
	@echo "test           Run tests"
	@echo "test-cov       Run tests with coverage report"
	@echo "lint           Run linting (flake8)"
	@echo "format         Format code with black"
	@echo "format-check   Check code formatting without changes"
	@echo "type-check     Run type checking with mypy"
	@echo "security       Run security checks"
	@echo "clean          Clean build artifacts"
	@echo "build          Build distribution packages"
	@echo "publish        Publish to PyPI (requires authentication)"
	@echo "docs           Build documentation"
	@echo "all            Run all checks (lint, type-check, test)"

install:
	$(PIP) install -e .

install-dev:
	$(PIP) install --upgrade pip setuptools wheel
	$(PIP) install -e .[dev,clipboard,docs]
	pre-commit install

test:
	$(PYTEST) -v

test-cov:
	$(PYTEST) -v --cov --cov-report=html --cov-report=term

test-integration:
	$(PYTEST) -v -m integration

lint:
	$(FLAKE8) src tests

format:
	$(BLACK) src tests

format-check:
	$(BLACK) --check src tests

type-check:
	$(MYPY) src

security:
	$(BANDIT) -r src
	$(SAFETY) check

clean:
	rm -rf build/
	rm -rf dist/
	rm -rf *.egg-info
	rm -rf .coverage
	rm -rf htmlcov/
	rm -rf .pytest_cache/
	rm -rf .mypy_cache/
	find . -type d -name __pycache__ -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

build: clean
	$(PYTHON) -m build

publish: build
	$(PYTHON) -m twine check dist/*
	$(PYTHON) -m twine upload dist/*

docs:
	cd docs && $(MAKE) clean && $(MAKE) html

# Run all checks
all: format-check lint type-check security test

# Development workflow
dev: format lint type-check test

# Quick test during development
quick: format test

# Pre-commit checks
pre-commit: format-check lint type-check test
