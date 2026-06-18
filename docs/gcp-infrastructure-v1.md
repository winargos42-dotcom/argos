# GCP Infrastructure — ARGOS v1.0 (Фаза 1 завершена)
## Project: argos-489214
## Billing: $300 Free Credit до 31.08.2026
## Alert: $250 (50% + 90%)

---

## ✅ Создано (09.06.2026)

### Cloud Storage
- **Bucket**: `gs://argos-489214-audit-logs`
- **Location**: us-central1
- **Access**: Uniform bucket-level

### Cloud SQL — MemPalace DB
- **Instance**: argos-mempalace
- **Engine**: PostgreSQL 15.17
- **Tier**: db-g1-small (2 vCPU, 1.7GB RAM)
- **Public IP**: 35.223.220.12
- **Connection**: `argos-489214:us-central1:argos-mempalace`
- **Database**: `argos_db`
- **User**: `argos_user`
- **Password**: `Argos20260609` (фиксирован, записан)
- **Backup**: daily 03:00
- **SSL**: required

### Compute Engine — API Server
- **Instance**: argos-api-server
- **Zone**: us-central1-a
- **Machine**: e2-medium (2 vCPU, 4GB RAM)
- **External IP**: 136.119.147.118
- **Internal IP**: 10.128.0.9
- **OS**: Debian 12
- **Disk**: 50GB pd-balanced
- **Docker**: ✅ installed
- **SSH**: `gcloud compute ssh argos-api-server`

### Firewall
- **Rule**: `argos-api-allow-http`
- **Ports**: 80, 443, 5000, 8000
- **Target**: VMs с тегом `argos-api`

---

## ✅ Проверено

### VM ↔ SQL connectivity
```bash
gcloud compute ssh argos-api-server --zone=us-central1-a --command="\
  PGPASSWORD='***' psql -h 35.223.220.12 -U argos_user -d argos_db -c 'SELECT version();'"
# → PostgreSQL 15.17 on x86_64-pc-linux-gnu
```

### Port reachability
```bash
# VM → SQL port 5432: REACHABLE ✅
# SQL public IP authorized for VM external IP
```

---

## 💰 Бюджет

| Ресурс | Месяц |
|--------|-------|
| e2-medium VM | ~$25 |
| db-g1-small SQL | ~$15 |
| Storage + egress | ~$1 |
| **Итого/мес** | **~$41** |
| 2.5 мес (до 31.08) | **~$102** |
| **Остаток** | **~$198** |

---

## 📋 Следующие шаги

1. [ ] **Deploy FastAPI** на `argos-api-server` (Docker / systemd)
2. [ ] **Cloud SQL Proxy** на VM для secure connections
3. [ ] **Cloud Run** — Telegram webhook service
4. [ ] **Cloud Monitoring** — метрики + алерты
5. [ ] **Cloud Build** — CI/CD pipeline

## 🔗 Quick Commands

```bash
# SSH to API server
gcloud compute ssh argos-api-server --zone=us-central1-a

# SQL proxy (Cloud SQL Connector)
wget https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.14.0/cloud-sql-proxy.linux.amd64
chmod +x cloud-sql-proxy
./cloud-sql-proxy --private-ip argos-489214:us-central1:argos-mempalace

# Direct psql from VM
psql -h 35.223.220.12 -U argos_user -d argos_db

# Check budget
gcloud billing budgets list
```
