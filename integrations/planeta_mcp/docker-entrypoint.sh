#!/bin/sh
set -eu

if [ "$(id -u)" = "0" ]; then
    mkdir -p /data/planeta
    chown -R app:app /data/planeta
    exec gosu app "$@"
fi

exec "$@"
