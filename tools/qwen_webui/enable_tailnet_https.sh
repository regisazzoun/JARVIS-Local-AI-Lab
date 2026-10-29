#!/bin/sh
# Requires HTTPS/Serve enabled in the existing tailnet administrator console.
# Never use Funnel (public Internet) for this mission.
set -eu
sudo timeout 20 tailscale serve --bg --yes --https=443 http://127.0.0.1:8088
# Keep HTTP until HTTPS is verified with the normal system trust store.
curl --fail --max-time 15 https://jarvis-macmini.tail805e83.ts.net/api/version
sudo tailscale serve --http=80 off
