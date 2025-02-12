.DEFAULT_GOAL := help

HOST ?= 0.0.0.0
PORT ?= 8000

run: ## Run the application using uvicorn with provided arguments or defaults
	poetry run uvicorn src.main:app --host $(HOST) --port $(PORT) --reload

install: ## Install a dependency using poetry
	@echo "Installing dependency $(LIBRARY)"
	poetry add $(LIBRARY)

uninstall: ## Uninstall a dependency using poetry
	@echo "Uninstall dependency $(LIBRARY)"
	poetry remove $(LIBRARY)

# DOCKER
up:
	docker compose up -d

down:
	docker compose down


# ALEMBIC MIGRATIONS
alembic-migration-init: # Create alembic template for migrations
	alembic init migrations

alembic-migration-history: # Show all alembic migrations
	alembic history --verbose

alembic-migration-generate: # Generate migrations with message
	alembic revision --autogenerate -m "$(m)"

alembic-migration-upgrade: # Apply all migrations
	alembic upgrade head

alembic-migration-downgrade: # downgrade -1 migration
	alembic downgrade -1

alembic-migration-downgrade-base: # downgrade all migrations
	alembic downgrade base


# LINTERS
ruff-check:
	poetry run ruff check .

ruff-fix:
	poetry run ruff check . --fix

help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z0-9_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-20s %s\n", $$1, $$2}'
