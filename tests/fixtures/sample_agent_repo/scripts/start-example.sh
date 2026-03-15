#!/usr/bin/env bash
set -eu

PORT="${PORT:-3000}"
PID_FILE="tmp/example.pid"

mkdir -p logs tmp
nohup node src/server.js > logs/server.log 2>&1 &
echo "$!" > "$PID_FILE"
chmod 600 "$PID_FILE"
