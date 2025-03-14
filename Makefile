include .env
export $(shell sed 's/=.*//' .env)

.DEFAULT_GOAL := help

APP_SERVICE = api
DB_SERVICE = db
PROXY_SERVICE = nginx

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

api-restart: ## Restart only api
	${DC} restart ${APP_SERVICE}

api-logs: ## Show logs only api
	${DC} logs --follow ${APP_SERVICE}

api-shell: ## Go to the api shell
	${DC} exec ${APP_SERVICE} /bin/bash

db-restart: ## Restart only api
	${DC} restart ${DB_SERVICE}

db-logs: ## Show logs only database
	${DC} logs --follow ${DB_SERVICE}

db-shell: ## Go to the db shell
	${DC} exec ${APP_SERVICE} /bin/bash

db-psql: ## Go to the psql
	${DC} exec ${DB_SERVICE} psql -U ${POSTGRES_USER} -d ${POSTGRES_DB} -p ${POSTGRES_PORT}

db-destroy: ## Delete volume database
	docker volume rm pomodoro-time_pg_data

proxy-restart: ## Restart only proxy server
	${DC} restart ${PROXY_SERVICE}

proxy-reload: ## Restart only proxy server
	${DC} exec ${PROXY_SERVICE} nginx -s reload

proxy-shell: ## Go to the api shell
	${DC} exec ${PROXY_SERVICE} /bin/sh

proxy-logs:
	${DC} logs --follow ${PROXY_SERVICE}

# Prod
prod-up: ## Build and run all services
	${DC} -f docker-compose.prod.yaml up --build -d

prod-down: ## Build and run all services
	${DC} -f docker-compose.prod.yaml down


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
	${DC} exec ${APP_SERVICE} ruff check .

ruff-fix:
	${DC} exec ${APP_SERVICE} ruff check . --fix

# MANAGEMENT
generate-dummy-data:
	${DC} exec ${APP_SERVICE} python3 src/management/dummy_data/generate_data.py


# TESTS
.PHONY: tests
tests: # Run all tests
	${DC} exec ${APP_SERVICE}  pytest tests

.PHONY: tests
tests-integrations: # Run all tests
	${DC} exec ${APP_SERVICE}  pytest tests -m "integration"

.PHONY: tests
tests-unittest: # Run all tests
	${DC} exec ${APP_SERVICE}  pytest tests -m "unittest"

tests-coverage:
	${DC} exec -T ${APP_SERVICE} pytest --cov=. .

tests-coverage-html:
	pytest --cov-report html:cov_html --cov=src tests/

# HELP
help: ## Show this help message
	@echo "Usage: make [command]"
	@echo ""
	@echo "Commands:"
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(firstword $(MAKEFILE_LIST)) | awk 'BEGIN {FS = ":.*?## "}; {printf "  %-40s %s\n", $$1, $$2}'
