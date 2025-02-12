#!/bin/bash
set -e

# Waiting until PostgreSQL becomes available
until pg_isready -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"; do
  echo "Waiting for PostgreSQL to become available..."
  sleep 2
done

# Creating additional test database
psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}"  -tc "SELECT 1 FROM pg_database WHERE datname = 'test_${POSTGRES_DB}'" | grep -q 1 || \
psql -U "${POSTGRES_USER}" -d "${POSTGRES_DB}" -c "CREATE DATABASE test_${POSTGRES_DB};"
