.PHONY: help install start stop restart clean lint test

# Default profile if none is given
PROFILE ?= none

# Variables
PYTHON = python3
PIP = pip3
DOCKER_COMPOSE = docker-compose
COMPOSE_FILES = -f docker-compose.yml -f supabase/docker/docker-compose.yml -f litellm/docker-compose.yml
PROJECT = local-ai-stack

help:
	@echo "Available commands:"
	@echo "  make install     - Install project dependencies"
	@echo "  make start       - Start all services"
	@echo "  make stop        - Stop all services"
	@echo "  make restart     - Restart all services"
	@echo "  make clean       - Clean up temporary files"
	@echo "  make lint        - Run linting checks"
	@echo "  make test        - Run tests"

install:
	$(PIP) install -r requirements.txt
	$(PIP) install -e .

pull:
	$(DOCKER_COMPOSE) -p $(PROJECT) --profile $(PROFILE) $(COMPOSE_FILES) pull

start:
	$(PYTHON) start_services.py --profile $(PROFILE)

stop:
	$(DOCKER_COMPOSE) -p $(PROJECT) --profile $(PROFILE) $(COMPOSE_FILES) down

restart: stop start

update:
	$(MAKE) stop PROFILE=$(PROFILE)
	$(MAKE) pull PROFILE=$(PROFILE)
	$(MAKE) start PROFILE=$(PROFILE)

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
	find . -type d -name ".mypy_cache" -exec rm -rf {} +
	find . -type d -name ".ruff_cache" -exec rm -rf {} +
	rm -rf dist/ build/

lint:
	ruff check .
	mypy .

test:
	pytest