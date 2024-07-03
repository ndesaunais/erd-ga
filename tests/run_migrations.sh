#! /usr/bin/env bash

set -euo pipefail

MIGRATION_DIR="$1"
for file in "${MIGRATION_DIR}"/*; do
  PGPASSWORD="${POSTGRES_PASSWORD}" psql -U "${POSTGRES_USER}" -h "${POSTGRES_HOST}" -p "${POSTGRES_PORT}" -d "${POSTGRES_DB}" -f "${file}"
done
