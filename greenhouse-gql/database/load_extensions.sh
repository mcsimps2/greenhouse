#!/bin/sh

set -e

# Perform all actions as $POSTGRES_USER
export PGUSER="$POSTGRES_USER"

echo "Loading extensions into $POSTGRES_DB"
"${psql[@]}" --dbname="$POSTGRES_DB" <<-'EOSQL'
  CREATE EXTENSION IF NOT EXISTS "pg_trgm";
  CREATE EXTENSION IF NOT EXISTS "btree_gin";
  CREATE EXTENSION IF NOT EXISTS "fuzzystrmatch";
  CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
EOSQL
