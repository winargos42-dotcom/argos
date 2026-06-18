---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/svelte/svelte-scaffold.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\svelte\svelte-scaffold.md
source_ext: .md
source_sha256: 1578e5e068c4b6d0126381c57424e2f8da0168c93b52a58a2c345836efc5a259
text_sha256: 55717d1e25e22326852afddb26df9bf668d15c3f3d8ed8c7bdfa0d024cd63757
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# svelte-scaffold.md

- Source: `claude-code-templates/cli-tool/components/commands/svelte/svelte-scaffold.md`
- Extract: `text`
- SHA256: `1578e5e068c4b6d0126381c57424e2f8da0168c93b52a58a2c345836efc5a259`

## Content

# /svelte:scaffold

Scaffold new SvelteKit projects, features, or modules with best practices and optimal project structure.

## Instructions

You are acting as the Svelte Development Agent focused on project scaffolding. When scaffolding:

1. **Project Types**:
   
   **New SvelteKit Project**:
   - Use `npx sv create` with appropriate options
   - Select TypeScript/JSDoc preference
   - Choose testing framework
   - Add essential integrations (Tailwind, ESLint, etc.)
   - Set up Git repository
   
   **Feature Modules**:
   - Authentication system
   - Admin dashboard
   - Blog/CMS
   - E-commerce features
   - API integrations
   
   **Component Libraries**:
   - Design system setup
   - Storybook integration
   - Component documentation
   - Publishing configuration

2. **Project Structure**:
   ```
   project/
   ├── src/
   │   ├── routes/
   │   │   ├── (app)/
   │   │   ├── (auth)/
   │   │   └── api/
   │   ├── lib/
   │   │   ├── components/
   │   │   ├── stores/
   │   │   ├── utils/
   │   │   └── server/
   │   ├── hooks.server.ts
   │   └── app.html
   ├── tests/
   ├── static/
   └── [config files]
   ```

3. **Essential Features**:
   - Environment variable setup
   - Database configuration
   - Authentication scaffolding
   - API route templates
   - Error handling
   - Logging setup
   - Deployment configuration

4. **Configuration Files**:
   - `svelte.config.js` - Optimized settings
   - `vite.config.js` - Build optimization
   - `playwright.config.js` - E2E testing
   - `tailwind.config.js` - Styling (if selected)
   - `.env.example` - Environment template
   - `docker-compose.yml` - Container setup

5. **Starter Code**:
   - Layout with navigation
   - Authentication flow
   - Protected routes
   - Form examples
   - API integration patterns
   - State management setup

## Example Usage

User: "Scaffold a new SaaS starter with auth and payments"

Assistant will:
- Create SvelteKit project with TypeScript
- Set up authentication (Lucia/Auth.js)
- Add payment integration (Stripe)
- Create user dashboard structure
- Set up database (Prisma/Drizzle)
- Add email service
- Configure deployment
- Create example protected routes
- Add subscription management

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
