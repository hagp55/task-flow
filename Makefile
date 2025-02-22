include .env
export $(shell sed 's/=.*//' .env)

.DEFAULT_GOAL := help

APP_SERVICE = api
DB_SERVICE = db

DC = docker compose
EXEC = docker exec -it
LOGS = docker logs


# DOCKER
up: ## Build and run all services
	${DC} up --build -d

build: ## Rebuild all services
	${DC} --build

full-build: ## Rebuild all services and refresh cache
	${DC} build --no-cache

restart: ## Restart all services
	${DC} restart

down: ## Down all services
	docker compose down

logs: ## Show logs all services
	${DC} logs --follow

api-logs: ## Show logs only api
	${DC} logs --follow ${APP_SERVICE}

api-shell: ## Go to the api shell
	${DC} exec ${APP_SERVICE} /bin/bash

db-logs: ## Show logs only database
	${DC} logs --follow ${DB_SERVICE}


db-shell: ## Go to the db shell
	${DC} exec ${APP_SERVICE} /bin/bash

db-psql: ## Go to the psql
	${DC} exec ${DB_SERVICE} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -p ${POSTGRES_PORT}

db-destroy: ## Delete volume database
	docker volume rm pomodoro-time_pg_data


# ALEMBIC MIGRATIONS
alembic-migration-init: ## Create alembic template for migrations
	${DC} exec ${APP_SERVICE} alembic init migrations

alembic-migration-history: ## Show all alembic migrations
	${DC} exec ${APP_SERVICE} alembic history --verbose

alembic-migration-generate: ## Generate migrations with message
	${DC} exec ${APP_SERVICE} alembic revision --autogenerate -m "$(m)"

alembic-migration-upgrade: ## Apply all migrations
	${DC} exec ${APP_SERVICE} alembic upgrade head

alembic-migration-downgrade: ## downgrade -1 migration
	${DC} exec ${APP_SERVICE} alembic downgrade -1

alembic-migration-downgrade-base: ## downgrade all migrations
	${DC} exec ${APP_SERVICE} alembic downgrade base


# LINTERS
ruff-check:
	poetry run ruff check .

ruff-fix:
	poetry run ruff check . --fix


# TESTS
.PHONY: tests
tests: # Run all tests
	pytest tests -vs


# HELP
help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-40s %s\n", $$1, $$2}'
