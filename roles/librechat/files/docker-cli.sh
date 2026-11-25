#!/bin/sh
set -eu

if [ -w /var/run/docker.sock ]; then
    exec /usr/bin/docker "$@"
fi
exec sudo -n /usr/bin/docker "$@"
