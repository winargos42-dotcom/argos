#!/usr/bin/env bash
set -euo pipefail

# Chrome/Chromium binds its remote debugging socket to loopback for safety.
# Expose it only inside the Railway private network on 9223 so the isolated
# controller service can connect. The public GUI remains separately protected.
exec socat TCP-LISTEN:9223,reuseaddr,fork,bind=0.0.0.0 TCP:127.0.0.1:9222
