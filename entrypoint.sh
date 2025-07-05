#!/bin/sh

echo "🚀 Starting main entrypoint..."

# 1. Run the Postgres initialization script (tables, functions, triggers)
echo "▶️ Running postgresql_entrypoint.py"
python ./database/postgresql/entrypoints/postgresql_entrypoint.py
echo "✅ postgresql_entrypoint.py finished"

# 2. Start Redis listener in background
echo "▶️ Starting redis_listener_entrypoint.sh in background"
./database/redis/entrypoints/redis_listener_entrypoint.sh &

# 3. Wait to keep container running
wait