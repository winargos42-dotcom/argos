# GCP Infrastructure — ARGOS
## Project: argos-489214
## Billing: $300 Free Credit (expires 31.08.2026)
## Alert: $250 threshold (50% + 90%)

---

## Cloud Storage
- Bucket: gs://argos-489214-audit-logs
- Location: us-central1
- Access: Uniform bucket-level

## Cloud SQL (MemPalace DB)
- Instance: argos-mempalace
- Engine: PostgreSQL 15.17
- Tier: db-g1-small (2 vCPU, 1.7GB RAM)
- Region: us-central1
- Public IP: 35.223.220.12
- Private IP: 10.126.0.3
- Connection name: argos-489214:us-central1:argos-mempalace
- Database: argos_db
- User: argos_user
- Password: Argos20260609
- SSL: required (server CA cert available via gcloud)
- Backup: daily 03:00

### Connection Strings
```
# Direct TCP (requires authorized network)
postgresql://argos_user:Argos20260609@35.223.220.12:5432/argos_db

# Cloud SQL Proxy (recommended for apps)
./cloud-sql-proxy argos-489214:us-central1:argos-mempalace
# Then connect to localhost:5432
```

## Compute Engine
- Instance: argos-api-server
- Zone: us-central1-a
- Machine: e2-medium (2 vCPU, 4GB RAM)
- External IP: 136.119.147.118
- Internal IP: 10.128.0.9
- OS: Debian 12
- Disk: 50GB pd-balanced
- Tags: http-server, https-server, argos-api
- Labels: env=prod, project=argos, phase=1
- Docker: installed (startup-script)
- SSH: gcloud compute ssh argos-api-server

---

## Pricing Estimate
| Resource | Monthly |
|----------|---------|
| e2-medium VM | ~$25 |
| db-g1-small SQL | ~$15 |
| 10GB storage | ~$0.50 |
| Egress (est 5GB) | ~$0.60 |
| **Total** | **~$41/mo** |
| 2.5 months | **~$102** |

Remaining credit: ~$198 for scaling

## Next Steps
1. [ ] Deploy FastAPI to argos-api-server via Docker
2. [ ] Connect API to Cloud SQL
3. [ ] Create Cloud Run service for Telegram webhook
4. [ ] Configure firewall rules for VM
5. [ ] Enable Cloud Monitoring

## Commands Reference
```bash
# SSH to VM
gcloud compute ssh argos-api-server --zone=us-central1-a

# SQL proxy
wget https://storage.googleapis.com/cloud-sql-connectors/cloud-sql-proxy/v2.14.0/cloud-sql-proxy.linux.amd64 -O cloud-sql-proxy
chmod +x cloud-sql-proxy
./cloud-sql-proxy --private-ip argos-489214:us-central1:argos-mempalace

# List VMs
gcloud compute instances list

# List SQL
gcloud sql instances list
```
