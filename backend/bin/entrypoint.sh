#!/bin/bash

#-----------------------------------------------------------
# Make sure you also update the relevant `command`s in     |
# docker-compose.yml when updating this                    |
#-----------------------------------------------------------

set -euo pipefail

script_name=$(basename "$0")

# utility function that prints its arguments to stderr with a prefix.
function log() {
  echo "$@" | sed 's/^/'"$script_name"': /' >&2
}

if [ $# -gt 0 ]; then
  exec "$@"
fi

GUNICORN_WORKERS=${GUNICORN_WORKERS:-5}
BACKEND_MODE=${BACKEND_MODE:-"<none>"}

log "starting backend with BACKEND_MODE=${BACKEND_MODE}"
case "$BACKEND_MODE" in
serve-grpc)
  exec python /app/backend/grpc-server.py
  ;;
serve-http)
  exec run-program gunicorn \
    --bind=0.0.0.0:5000 \
    --access-logfile=- \
    --threads=4 \
    --access-logformat="%(h)s %(l)s %(u)s %(t)s \"%(r)s\" %(s)s %(b)s \"%(f)s\" \"%(a)s\" %(L)s" \
    --workers="${GUNICORN_WORKERS}" \
    --timeout=600 \
    --limit-request-field_size=65520 \
    --limit-request-line=8188 \
    app:app
  ;;
*)
  log "can't start backend with BACKEND_MODE=${BACKEND_MODE}"
  exit 1
esac