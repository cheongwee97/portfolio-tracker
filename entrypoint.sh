#!/bin/sh

# Set exit on error
set -e

echo "Starting portfolio tracker database initialization..."

# Wait for PostgreSQL to be ready (if using external DB)
echo "Waiting for database connection..."

# Run the Python initialization script
echo "Running database entrypoint initialization..."
python database/postgresql/postgresql_init.py

echo "Portfolio tracker database initialization completed successfully!"

# Keep container running or execute additional commands
exec "$@"