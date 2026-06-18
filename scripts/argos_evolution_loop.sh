#!/bin/bash
# ARGOS Evolution Loop - непрерывное обучение + мониторинг
# Запускается через systemd timer каждые 30 мин

set -e
PROJECT_ROOT="/home/ava/Projects/argoss"
VENV="$PROJECT_ROOT/.venv/bin"
LOG_FILE="$PROJECT_ROOT/logs/evolution_loop.log"

echo "=================================================" >> "$LOG_FILE"
echo "  $(date) — Evolution Loop START" >> "$LOG_FILE"
echo "=================================================" >> "$LOG_FILE"

cd "$PROJECT_ROOT"

# 1. Generate new training dataset
echo "" >> "$LOG_FILE"
echo "1. Train dataset..." >> "$LOG_FILE"
"$VENV/python3" scripts/argos_train_from_chats.py >> "$LOG_FILE" 2>&1

# 2. Train BM25 model
echo "" >> "$LOG_FILE"
echo "2. Train BM25 model..." >> "$LOG_FILE"
"$VENV/python3" scripts/argos_local_train_v2.py >> "$LOG_FILE" 2>&1

# 3. Evolution v2 cycle
echo "" >> "$LOG_FILE"
echo "3. Evolution cycle..." >> "$LOG_FILE"
"$VENV/python3" scripts/evolution_v2.py >> "$LOG_FILE" 2>&1

# 4. Unified dashboard
echo "" >> "$LOG_FILE"
echo "4. Dashboard update..." >> "$LOG_FILE"
"$VENV/python3" scripts/argos_unified_dashboard.py >> "$LOG_FILE" 2>&1

# 5. Submit evidence to Veto
echo "" >> "$LOG_FILE"
echo "5. Veto evidence..." >> "$LOG_FILE"
"$VENV/python3" << EOF >> "$LOG_FILE" 2>&1
import sys
sys.path.insert(0, '$PROJECT_ROOT/scripts')
sys.path.insert(0, '$PROJECT_ROOT/src/audit')
from argos_council_integration import CouncilTrustGuard
from veto_protocol import VetoEvidence
g = CouncilTrustGuard()
ev = VetoEvidence(node_id='laptop', metric_name='evolution_loop_run', value=0.95, severity=0.3, source='evolution_loop')
r = g.submit_evidence(ev)
print(f"  Veto evidence: trust={r.get('confidence', '?')}")
EOF

echo "" >> "$LOG_FILE"
echo "$(date) — Evolution Loop END ✅" >> "$LOG_FILE"
echo "=================================================" >> "$LOG_FILE"
echo "" >> "$LOG_FILE"
