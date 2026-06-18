---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/r2-sql/configuration.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\r2-sql\configuration.md
source_ext: .md
source_sha256: 841d5c71f4206517b8aed9066739e6e3767ceae6e9f23b9af2cd51a842f0dc82
text_sha256: c7f20114aad49340e78cf493404fecbe53a8c835b428f3c52900f37c82ba83da
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# configuration.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/r2-sql/configuration.md`
- Extract: `text`
- SHA256: `841d5c71f4206517b8aed9066739e6e3767ceae6e9f23b9af2cd51a842f0dc82`

## Content

# R2 SQL Configuration

Setup and configuration for R2 SQL queries.

## Prerequisites

- R2 bucket with Data Catalog enabled
- API token with R2 permissions
- Wrangler CLI installed (for CLI queries)

## Enable R2 Data Catalog

R2 SQL queries Apache Iceberg tables in R2 Data Catalog. Must enable catalog on bucket first.

### Via Wrangler CLI

```bash
npx wrangler r2 bucket catalog enable <bucket-name>
```

Output includes:
- **Warehouse name** - Typically same as bucket name
- **Catalog URI** - REST endpoint for catalog operations

Example output:
```
Catalog enabled successfully
Warehouse: my-bucket
Catalog URI: https://abc123.r2.cloudflarestorage.com/iceberg/my-bucket
```

### Via Dashboard

1. Navigate to **R2 Object Storage** → Select your bucket
2. Click **Settings** tab
3. Scroll to **R2 Data Catalog** section
4. Click **Enable**
5. Note the **Catalog URI** and **Warehouse** name

**Important:** Enabling catalog creates metadata directories in bucket but does not modify existing objects.

## Create API Token

R2 SQL requires API token with R2 permissions.

### Required Permission

**R2 Admin Read & Write** (includes R2 SQL Read permission)

### Via Dashboard

1. Navigate to **R2 Object Storage**
2. Click **Manage API tokens** (top right)
3. Click **Create API token**
4. Select **Admin Read & Write** permission
5. Click **Create API Token**
6. **Copy token value** - shown only once

### Permission Scope

| Permission | Grants Access To |
|------------|------------------|
| R2 Admin Read & Write | R2 storage operations + R2 SQL queries + Data Catalog operations |
| R2 SQL Read | SQL queries only (no storage writes) |

**Note:** R2 SQL Read permission not yet available via Dashboard - use Admin Read & Write.

## Configure Environment

### Wrangler CLI

Set environment variable for Wrangler to use:

```bash
export WRANGLER_R2_SQL_AUTH_TOKEN=<your-token>
```

Or create `.env` file in project directory:

```
WRANGLER_R2_SQL_AUTH_TOKEN=<your-token>
```

Wrangler automatically loads `.env` file when running commands.

### HTTP API

For programmatic access (non-Wrangler), pass token in Authorization header:

```bash
curl -X POST https://api.cloudflare.com/client/v4/accounts/{account_id}/r2/sql/query \
  -H "Authorization: Bearer <your-token>" \
  -H "Content-Type: application/json" \
  -d '{
    "warehouse": "my-bucket",
    "query": "SELECT * FROM default.my_table LIMIT 10"
  }'
```

**Note:** HTTP API endpoint URL may vary - see [patterns.md](patterns.md#http-api-query) for current endpoint.

## Verify Setup

Test configuration by querying system tables:

```bash
# List namespaces
npx wrangler r2 sql query "my-bucket" "SHOW DATABASES"

# List tables in namespace
npx wrangler r2 sql query "my-bucket" "SHOW TABLES IN default"
```

If successful, returns JSON array of results.

## Troubleshooting

### "Token authentication failed"

**Cause:** Invalid or missing token

**Solution:**
- Verify `WRANGLER_R2_SQL_AUTH_TOKEN` environment variable set
- Check token has Admin Read & Write permission
- Create new token if expired

### "Catalog not enabled on bucket"

**Cause:** Data Catalog not enabled

**Solution:**
- Run `npx wrangler r2 bucket catalog enable <bucket-name>`
- Or enable via Dashboard (R2 → bucket → Settings → R2 Data Catalog)

### "Permission denied"

**Cause:** Token lacks required permissions

**Solution:**
- Verify token has **Admin Read & Write** permission
- Create new token with correct permissions

## See Also

- [r2-data-catalog/configuration.md](../r2-data-catalog/configuration.md) - Detailed token setup and PyIceberg connection
- [patterns.md](patterns.md) - Query examples using configuration
- [gotchas.md](gotchas.md) - Common configuration errors

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
