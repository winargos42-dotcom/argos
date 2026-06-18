---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/netlify-deploy/references/cli-commands.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\netlify-deploy\references\cli-commands.md
source_ext: .md
source_sha256: fda11991e7e3639608f4d9683fadc68c969fa2b0897c7d87b3e027c5b0737a80
text_sha256: a24b08401b8c796e4a58933a71441b3341b61afc840d690d9127b27ab00cfe05
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:45
---

# cli-commands.md

- Source: `claude-code-templates/cli-tool/components/skills/development/netlify-deploy/references/cli-commands.md`
- Extract: `text`
- SHA256: `fda11991e7e3639608f4d9683fadc68c969fa2b0897c7d87b3e027c5b0737a80`

## Content

# Netlify CLI Commands Reference

Quick reference for common Netlify CLI commands used in deployments.

## Authentication

```bash
# Login via browser OAuth
npx netlify login

# Check authentication status and site link
npx netlify status

# Logout
npx netlify logout
```

## Site Management

```bash
# Link current directory to existing site
npx netlify link

# Link by Git remote URL
npx netlify link --git-remote-url <url>

# Create and link new site
npx netlify init

# Unlink from current site
npx netlify unlink

# Open site in Netlify dashboard
npx netlify open

# Open site admin panel
npx netlify open:admin

# Open site in browser
npx netlify open:site
```

## Deployment

```bash
# Deploy preview/draft (safe for testing)
npx netlify deploy

# Deploy to production
npx netlify deploy --prod

# Deploy with specific directory
npx netlify deploy --dir=dist

# Deploy with message
npx netlify deploy --message="Deploy message"

# List all deploys
npx netlify deploy:list
```

## Development

```bash
# Run local dev server with Netlify features
npx netlify dev

# Run local dev server on specific port
npx netlify dev --port 3000
```

## Site Information

```bash
# Get site info
npx netlify sites:list

# Get current site info
npx netlify api getSite --data '{"site_id": "YOUR_SITE_ID"}'
```

## Environment Variables

```bash
# List environment variables
npx netlify env:list

# Set environment variable
npx netlify env:set KEY value

# Get environment variable value
npx netlify env:get KEY

# Import env vars from file
npx netlify env:import .env
```

## Build

```bash
# Show build settings
npx netlify build --dry

# Run build locally
npx netlify build
```

## Functions (Serverless)

```bash
# List functions
npx netlify functions:list

# Invoke function locally
npx netlify functions:invoke FUNCTION_NAME

# Create new function
npx netlify functions:create FUNCTION_NAME
```

## Logs

```bash
# Stream function logs
npx netlify logs

# View logs for specific function
npx netlify logs:function FUNCTION_NAME
```

## Troubleshooting Commands

```bash
# Check CLI version
npx netlify --version

# Get help for any command
npx netlify help [command]

# Check status with verbose output
npx netlify status --verbose
```

## Exit Codes

- `0` - Success
- `1` - General error
- `2` - Authentication error
- `3` - Site not found
- `4` - Build failed

## Common Flags

- `--json` - Output as JSON
- `--silent` - Suppress output
- `--debug` - Show debug information
- `--force` - Skip confirmation prompts

## Resources

- Full CLI documentation: https://docs.netlify.com/cli/get-started/
- CLI GitHub repository: https://github.com/netlify/cli

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
