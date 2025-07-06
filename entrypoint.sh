#!/bin/sh
echo "🚀 Starting main entrypoint..."

# 1. Run the Postgres initialization script
echo "Running postgresql_entrypoint.py"
python -u ./database/postgresql/entrypoints/postgresql_entrypoint.py
echo "postgresql_entrypoint.py finished"

# 2. Start Redis listeners
echo "Starting redis_listener_entrypoint.sh"
exec ./database/redis/entrypoints/redis_listener_entrypoint.sh
