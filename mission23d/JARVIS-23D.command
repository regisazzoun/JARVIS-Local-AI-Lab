#!/bin/zsh
set -eu
port=8783
printf 'Ouverture du banc vocal JARVIS 23D…\n'
if curl --silent --fail --max-time 2 "http://127.0.0.1:${port}/" >/dev/null; then
  open "http://127.0.0.1:${port}/"
  exit 0
fi
ssh jarvis 'if ! curl -fsS --max-time 2 http://127.0.0.1:8783/health >/dev/null; then nohup /var/lib/jarvis/projects/mission23/livekit-agent/venv/bin/python /var/lib/jarvis/projects/mission23/mission23d/server.py > /var/lib/jarvis/projects/mission23/mission23d/logs/gateway.log 2>&1 < /dev/null & fi'
ssh -o ExitOnForwardFailure=yes -o ServerAliveInterval=15 \
  -N -L "127.0.0.1:${port}:127.0.0.1:${port}" \
  -L 127.0.0.1:7880:127.0.0.1:7880 \
  -L 127.0.0.1:7881:127.0.0.1:7881 jarvis &
tunnel_pid=$!
trap 'kill "$tunnel_pid" 2>/dev/null || true' EXIT INT TERM
for attempt in {1..30}; do
  if curl --silent --fail --max-time 2 "http://127.0.0.1:${port}/" >/dev/null; then
    open "http://127.0.0.1:${port}/"
    printf 'Gardez cette fenêtre ouverte pendant la conversation. Fermez-la pour arrêter le tunnel.\n'
    wait "$tunnel_pid"
    exit 0
  fi
  kill -0 "$tunnel_pid" 2>/dev/null || break
  sleep 1
done
printf 'La page temporaire ne répond pas encore sur JARVIS. Le tunnel a été arrêté.\n'
exit 1
