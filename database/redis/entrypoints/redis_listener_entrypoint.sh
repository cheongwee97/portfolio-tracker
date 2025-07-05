#!/bin/sh

echo "▶ Starting redis listener scripts..."

for script in database/redis/listeners/listener_*.py; do
  if [ -f "$script" ]; then
    echo "▶ Running $script"
    python "$script" &
  else
    echo "⚠️ No listener scripts found matching pattern."
  fi
done

wait