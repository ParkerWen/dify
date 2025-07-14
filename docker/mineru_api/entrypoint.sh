#!/usr/bin/env bash
set -euo pipefail

exec uvicorn app:app "$@"
