#!/bin/sh

echo "▶ Starting redis listener scripts..."

found=0

for script in database/redis/listeners/listener_*.py; do
  if [ -f "$script" ]; then
    found=1
    echo "Running $script"
    python -u "$script"
  fi
done

if [ "$found" -eq 0 ]; then
  echo "No listener scripts found matching pattern."
fi
