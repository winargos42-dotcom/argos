---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/terraform/api.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\terraform\api.md
source_ext: .md
source_sha256: 6ff81bc38fa36d364763c419649957d88a1e90b100f176bbe2b5fbe86f58137b
text_sha256: 5dc812c078d06454d801b0e126d50c48031c1a7b0ffef7ebf77a97cf7b41e768
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# api.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/terraform/api.md`
- Extract: `text`
- SHA256: `6ff81bc38fa36d364763c419649957d88a1e90b100f176bbe2b5fbe86f58137b`

## Content

# Terraform Data Sources Reference

Query existing Cloudflare resources to reference in your configurations.

## v5 Data Source Names

| v4 Name | v5 Name | Notes |
|---------|---------|-------|
| `cloudflare_record` | `cloudflare_dns_record` | |
| `cloudflare_worker_script` | `cloudflare_workers_script` | Note: plural |
| `cloudflare_access_*` | `cloudflare_zero_trust_*` | Access → Zero Trust |

## Zone Data Sources

```hcl
# Get zone by name
data "cloudflare_zone" "example" {
  name = "example.com"
}

# Use in resources
resource "cloudflare_dns_record" "www" {
  zone_id = data.cloudflare_zone.example.id
  name = "www"
  # ...
}
```

## Account Data Sources

```hcl
# List all accounts
data "cloudflare_accounts" "main" {
  name = "My Account"
}

# Use account ID
resource "cloudflare_worker_script" "api" {
  account_id = data.cloudflare_accounts.main.accounts[0].id
  # ...
}
```

## Worker Data Sources

```hcl
# Get existing worker script (v5: cloudflare_workers_script)
data "cloudflare_workers_script" "existing" {
  account_id = var.account_id
  name = "existing-worker"
}

# Reference in service bindings
resource "cloudflare_workers_script" "consumer" {
  service_binding {
    name = "UPSTREAM"
    service = data.cloudflare_workers_script.existing.name
  }
}
```

## KV Data Sources

```hcl
# Get KV namespace
data "cloudflare_workers_kv_namespace" "existing" {
  account_id = var.account_id
  namespace_id = "abc123"
}

# Use in worker binding
resource "cloudflare_workers_script" "api" {
  kv_namespace_binding {
    name = "KV"
    namespace_id = data.cloudflare_workers_kv_namespace.existing.id
  }
}
```

## Lists Data Source

```hcl
# Get IP lists for WAF rules
data "cloudflare_list" "blocked_ips" {
  account_id = var.account_id
  name = "blocked_ips"
}
```

## IP Ranges Data Source

```hcl
# Get Cloudflare IP ranges (for firewall rules)
data "cloudflare_ip_ranges" "cloudflare" {}

output "ipv4_cidrs" {
  value = data.cloudflare_ip_ranges.cloudflare.ipv4_cidr_blocks
}

output "ipv6_cidrs" {
  value = data.cloudflare_ip_ranges.cloudflare.ipv6_cidr_blocks
}

# Use in security group rules (AWS example)
resource "aws_security_group_rule" "allow_cloudflare" {
  type = "ingress"
  from_port = 443
  to_port = 443
  protocol = "tcp"
  cidr_blocks = data.cloudflare_ip_ranges.cloudflare.ipv4_cidr_blocks
  security_group_id = aws_security_group.web.id
}
```

## Common Patterns

### Import ID Formats

| Resource | Import ID Format |
|----------|------------------|
| `cloudflare_zone` | `<zone-id>` |
| `cloudflare_dns_record` | `<zone-id>/<record-id>` |
| `cloudflare_workers_script` | `<account-id>/<script-name>` |
| `cloudflare_workers_kv_namespace` | `<account-id>/<namespace-id>` |
| `cloudflare_r2_bucket` | `<account-id>/<bucket-name>` |
| `cloudflare_d1_database` | `<account-id>/<database-id>` |
| `cloudflare_pages_project` | `<account-id>/<project-name>` |

```bash
# Example: Import DNS record
terraform import cloudflare_dns_record.example <zone-id>/<record-id>
```

### Reference Across Modules

```hcl
# modules/worker/main.tf
data "cloudflare_zone" "main" {
  name = var.domain
}

resource "cloudflare_worker_route" "api" {
  zone_id = data.cloudflare_zone.main.id
  pattern = "api.${var.domain}/*"
  script_name = cloudflare_worker_script.api.name
}
```

### Output Important Values

```hcl
output "zone_id" {
  value = cloudflare_zone.main.id
  description = "Zone ID for DNS management"
}

output "worker_url" {
  value = "https://${cloudflare_worker_domain.api.hostname}"
  description = "Worker API endpoint"
}

output "kv_namespace_id" {
  value = cloudflare_workers_kv_namespace.app.id
  sensitive = false
}

output "name_servers" {
  value = cloudflare_zone.main.name_servers
  description = "Name servers for domain registration"
}
```

## See Also

- [README](./README.md) - Provider setup
- [Configuration Reference](./configuration.md) - All resource types
- [Patterns](./patterns.md) - Architecture patterns
- [Troubleshooting](./gotchas.md) - Common issues

<!-- ARGOS_MEMORY_WEB:START -->
## Связи памяти

- Центральный узел: [[ARGOS Memory Web]]
- Тематический узел: [[Project Mirror Hub]]
- Карта памяти: [[Карта памяти]]
- Контекст работы: [[Контекст работы]]
- Журнал MCP: [[2026-05-04 MCP Skill Audit]]
- Источник связи: `local-vault`
<!-- ARGOS_MEMORY_WEB:END -->

[[Backbone Hub]]

## Graph Bridge
- [[ARGOS Memory Web]]
- [[Backbone Hub]]
- [[Project Mirror Hub]]
