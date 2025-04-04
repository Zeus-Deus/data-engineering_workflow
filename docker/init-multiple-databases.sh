#!/bin/bash
set -e
set -u

function create_user_and_database() {
    local database=$1
    echo "  Creating user and database '$database'"
    psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" <<-EOSQL
        CREATE USER "$database" WITH PASSWORD '${POSTGRES_DEFAULT_USER_PASSWORD}';
        CREATE DATABASE "$database";
        GRANT ALL PRIVILEGES ON DATABASE "$database" TO "$database";
EOSQL
    if [ $? -eq 0 ]; then
        echo "  Successfully created user and database '$database'"
    else
        echo "  Failed to create user and database '$database'"
    fi
}

if [ -n "${POSTGRES_MULTIPLE_DATABASES:-}" ]; then
    echo "Multiple database creation requested: $POSTGRES_MULTIPLE_DATABASES"
    for db in $(echo $POSTGRES_MULTIPLE_DATABASES | tr ',' ' '); do
        create_user_and_database "$db"
    done
    echo "Multiple databases created"
else
    echo "No multiple database variable provided."
fi
