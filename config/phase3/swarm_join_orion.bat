:: ARGOS Phase 3 — Orion Swarm Join
:: Run as Administrator in PowerShell/cmd
:: Requires: Docker Desktop installed, WSL2 enabled
@echo off
echo ===== ARGOS Swarm Join: Orion =====
echo 1. Ensure Docker Desktop is running...
payloads
echo 2. Leaving any existing swarm...  docker swarm leave --force
echo 3. Joining swarm as worker...
:: TOKEN and IP will be filled by bootstrap
docker swarm join --token SWMTKN-1-55vkijtns5l610hahy16tjslsvzvjufl7nhr01fjygjt4ata9l-3q9jzawrleaj2q02hdhvxupct 192.168.2.1:2377
echo 4. Status:
docker info --format '{{json .Swarm}}' | python -m json.tool
echo ===== DONE =====
pause
