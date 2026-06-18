---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/render-deploy/references/direct-creation.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\render-deploy\references\direct-creation.md
source_ext: .md
source_sha256: 867a0dc4a4c5fbbdc65c48879a1f8902e14c072bcd723ef64cfe7887b771a5b0
text_sha256: 3b148def3c12061582229599616b680f57972c86a8782e22a765cf261ec80adc
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:46
---

# direct-creation.md

- Source: `claude-code-templates/cli-tool/components/skills/development/render-deploy/references/direct-creation.md`
- Extract: `text`
- SHA256: `867a0dc4a4c5fbbdc65c48879a1f8902e14c072bcd723ef64cfe7887b771a5b0`

## Content

# Direct Creation (MCP) Details

Use this reference for MCP direct-creation examples and follow-on configuration.

## Direct Creation Workflow

### Step 1: Analyze Codebase

Use [codebase-analysis.md](codebase-analysis.md) to determine runtime, build/start commands, env vars, and datastores.

### Step 2: Create Resources via MCP

**Create a Web Service:**
```
create_web_service(
  name: "my-api",
  runtime: "node",  # or python, go, rust, ruby, elixir, docker
  repo: "https://github.com/username/repo",
  branch: "main",  # optional, defaults to repo default branch
  buildCommand: "npm ci",
  startCommand: "npm start",
  plan: "free",  # free, starter, standard, pro, pro_max, pro_plus, pro_ultra
  region: "oregon",  # oregon, frankfurt, singapore, ohio, virginia
  envVars: [
    {"key": "NODE_ENV", "value": "production"}
  ]
)
```

**Create a Static Site:**
```
create_static_site(
  name: "my-frontend",
  repo: "https://github.com/username/repo",
  branch: "main",
  buildCommand: "npm run build",
  publishPath: "dist",  # or build, public, out
  envVars: [
    {"key": "VITE_API_URL", "value": "https://api.example.com"}
  ]
)
```

**Create a Cron Job:**
```
create_cron_job(
  name: "daily-cleanup",
  runtime: "node",
  repo: "https://github.com/username/repo",
  schedule: "0 0 * * *",  # Daily at midnight (cron syntax)
  buildCommand: "npm ci",
  startCommand: "node scripts/cleanup.js",
  plan: "free"
)
```

**Create a PostgreSQL Database:**
```
create_postgres(
  name: "myapp-db",
  plan: "free",  # free, basic_256mb, basic_1gb, basic_4gb, pro_4gb, etc.
  region: "oregon"
)
```

**Create a Key-Value Store (Redis):**
```
create_key_value(
  name: "myapp-cache",
  plan: "free",  # free, starter, standard, pro, pro_plus
  region: "oregon",
  maxmemoryPolicy: "allkeys_lru"  # eviction policy
)
```

### Step 3: Configure Environment Variables

After creating services, add environment variables:

```
update_environment_variables(
  serviceId: "<service-id-from-creation>",
  envVars: [
    {"key": "DATABASE_URL", "value": "<connection-string>"},
    {"key": "JWT_SECRET", "value": "<secret-value>"},
    {"key": "API_KEY", "value": "<api-key>"}
  ]
)
```

**Note:** For database connection strings, get the internal URL from the database details in Dashboard or via `get_postgres(postgresId: "<id>")`.

### Step 4: Verify Deployment

Services with `autoDeploy: "yes"` (default) will deploy automatically when created.

**Check deployment status:**
```
list_deploys(serviceId: "<service-id>", limit: 1)
```

**Monitor logs for errors:**
```
list_logs(resource: ["<service-id>"], level: ["error"], limit: 50)
```

**Check health metrics:**
```
get_metrics(
  resourceId: "<service-id>",
  metricTypes: ["http_request_count", "cpu_usage", "memory_usage"]
)
```

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
