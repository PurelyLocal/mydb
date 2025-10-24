#!/usr/bin/env bash
set -e
INTERVAL="${1:-30}"
while true; do
  git fetch --all --prune
  git reset --hard origin/main || true
  sleep "$INTERVAL"
done
