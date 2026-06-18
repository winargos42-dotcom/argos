#!/bin/bash
# ARGOS Phase 3 — Orange Pi Swarm Join
# Run as root on OPi

echo "===== ARGOS Swarm Join: OPi ====="
echo "1. Leaving any existing swarm..."
docker swarm leave --force 2>/dev/null
echo "2. Joining swarm as worker..."
# Token from Nexus manager
docker swarm join --token SWMTKN-1-55vkijtns5l610hahy16tjslsvzvjufl7nhr01fjygjt4ata9l-3q9jzawrleaj2q02hdhvxupct 192.168.2.1:2377
echo "3. Status:"
docker info --format '{{json .Swarm}}' | python3 -m json.tool
echo "===== DONE ====="
