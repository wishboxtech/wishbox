#!/bin/bash

# if any of the commands in your code fails for any reason, the entire script fails
set -o errexit
# fail exit if one of your pipe command fails
set -o pipefail
# exits if any of your variables is not set
set -o nounset

postgres_ready() {
python << END
import sys

import psycopg

try:
    psycopg.connect(
        dbname="${DEFAULT_DATABASE_NAME}",
        user="${DEFAULT_DATABASE_USER}",
        password="${DEFAULT_DATABASE_PASSWORD}",
        host="${DEFAULT_DATABASE_HOST}",
        port="${DEFAULT_DATABASE_PORT}",
    )
except psycopg.OperationalError:
    sys.exit(-1)
sys.exit(0)

END
}
until postgres_ready; do
  >&2 echo 'Waiting for PostgreSQL to become available...'
  sleep 1
done
>&2 echo 'PostgreSQL is available'

exec "$@"