#!/bin/bash

set -e

shift
cmd="$@"

until PGPASSWORD=$DB_PASSD psql -h ""$DB_HOST"" -p "$DB_PORT" -U "$DB_USER" -c '\q'; do
  >&2 echo "Postgres is unavailable - sleeping"
  sleep 1
done

>&2 echo "Postgres is up - executing command"

alembic revision --autogenerate -m "init"

alembic upgrade head

gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:8000

exec $cmd