---
argos_import: project_file
source_path: claude-code-templates/docu/docs/components/mcps.md
source_abs: F:\debug\argoss\claude-code-templates\docu\docs\components\mcps.md
source_ext: .md
source_sha256: 5c90f3c97f6dcf673caf2334f902b35f9a66ede5db6b25f275ae9764d49f4a6b
text_sha256: 9fd60c6068ed43df0c15668bcfcef945aee35aaa3697a65078e3da47e19b5c39
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:55
---

# mcps.md

- Source: `claude-code-templates/docu/docs/components/mcps.md`
- Extract: `text`
- SHA256: `5c90f3c97f6dcf673caf2334f902b35f9a66ede5db6b25f275ae9764d49f4a6b`

## Content

---
sidebar_position: 5
---

# MCPs (Model Context Protocol)

External service integrations that extend Claude Code with real-time data access. Browse and install from **[aitmpl.com](https://aitmpl.com)**.

## 🔌 What are MCPs?

MCPs connect Claude Code to external services, databases, and APIs. They provide real-time access to live data and services during conversations.

## Installation

### 📦 Basic Installation
Install this component locally in your project. Works with your existing Claude Code setup.

```bash
npx claude-code-templates@latest --mcp database/supabase --yes
```

### Multiple MCPs
```bash
npx claude-code-templates@latest --mcp database/supabase,development/github-integration --yes
```

## ⚙️ Configuration

Most MCPs require configuration after installation:

### API Keys
Add required API keys to environment variables:
```bash
# Database MCPs
DATABASE_URL=your_database_url
SUPABASE_URL=your_supabase_url
SUPABASE_ANON_KEY=your_anon_key

# GitHub MCP
GITHUB_TOKEN=your_github_token

# Cloud MCPs
AWS_ACCESS_KEY_ID=your_aws_key
AWS_SECRET_ACCESS_KEY=your_aws_secret
```

## 💡 Usage After Installation

MCPs provide real-time data access:
- **Query databases** directly in conversations
- **Access GitHub repos** and issues
- **Browse documentation** with context
- **Control browsers** for testing
- **Interact with cloud services**

## 📁 MCP Categories

Browse MCPs by integration type to connect Claude Code with external services:

### Database Integrations
Connect to databases and data sources for real-time data access. Examples: `supabase` for Supabase integration, `postgresql-integration` for PostgreSQL access, `mongodb-integration` for MongoDB queries.

### Development Tools
GitHub, version control, and development service connections. Examples: `github-integration` for repository access, `filesystem-access` for file operations, `npm-registry` for package management.

### Documentation & Context
Documentation and knowledge base access for contextual information. Examples: `context7` for documentation lookup, `confluence-integration` for enterprise wikis, `notion-integration` for team knowledge bases.

### Browser Automation
Web scraping and browser control for testing and automation. Examples: `playwright-mcp` for web automation, `browsermcp` for browser control, `selenium-integration` for legacy browser testing.

### Cloud Services
AWS, Google Cloud, and other cloud platform integrations. Examples: `aws-integration` for AWS services, `gcp-integration` for Google Cloud, `vercel-integration` for deployment management.

### Communication
Slack, Discord, and other communication tool connections. Examples: `slack-integration` for team communication, `discord-integration` for community management, `teams-integration` for enterprise chat.

## 🎯 How to Choose MCPs

Select MCPs based on your project's external service requirements:

### By Project Type
- **Web applications**: Choose `supabase` and `github-integration` for database and version control
- **Data projects**: Use `postgresql-integration` and `context7` for data access and documentation
- **API services**: Select `github-integration` and `aws-integration` for development and deployment
- **Testing projects**: Pick `playwright-mcp` and `filesystem-access` for automation and file handling

### By Data Requirements
- **Live database access**: Choose appropriate `database/*` MCPs for real-time queries
- **Documentation lookup**: Use `context7` for intelligent documentation search
- **Repository access**: Select `github-integration` for code and issue management
- **Web automation**: Pick `browser/*` MCPs for web scraping and testing

### By Integration Needs
- **Supabase projects**: Essential `supabase` MCP for database operations
- **GitHub workflows**: Required `github-integration` for repository management
- **AWS deployments**: Use `aws-integration` for cloud service management
- **Browser testing**: Select `playwright-mcp` for automated web testing

## 🔧 Pro Tips

- **Start with essential MCPs** for your stack
- **Configure environment variables** properly
- **Test connections** after installation
- **Browse [aitmpl.com](https://aitmpl.com)** for specialized integrations

---

**Find more MCPs:** [Browse all MCPs on aitmpl.com](https://aitmpl.com) → Filter by "MCPs"

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
