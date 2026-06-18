---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/svelte/svelte-storybook-setup.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\svelte\svelte-storybook-setup.md
source_ext: .md
source_sha256: 895490548db4b53047db3464df40608f9f21d9517b22837bbb0c370d383cf390
text_sha256: fb3ed0e84b109ec3a8a556756c284552627a84007906a8b0ec7750ab7abfab19
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# svelte-storybook-setup.md

- Source: `claude-code-templates/cli-tool/components/commands/svelte/svelte-storybook-setup.md`
- Extract: `text`
- SHA256: `895490548db4b53047db3464df40608f9f21d9517b22837bbb0c370d383cf390`

## Content

# /svelte:storybook-setup

Initialize and configure Storybook for SvelteKit projects with optimal settings and structure.

## Instructions

You are acting as the Svelte Storybook Specialist Agent focused on Storybook setup. When setting up Storybook:

1. **Installation Process**:
   
   **New Installation**:
   ```bash
   npx storybook@latest init
   ```
   
   **Manual Setup**:
   - Install core dependencies
   - Configure @storybook/sveltekit framework
   - Add essential addons
   - Set up Svelte CSF addon

2. **Configuration Files**:
   
   **.storybook/main.js**:
   ```javascript
   export default {
     stories: ['../src/**/*.stories.@(js|ts|svelte)'],
     addons: [
       '@storybook/addon-essentials',
       '@storybook/addon-svelte-csf',
       '@storybook/addon-a11y',
       '@storybook/addon-interactions'
     ],
     framework: {
       name: '@storybook/sveltekit',
       options: {}
     },
     staticDirs: ['../static']
   };
   ```
   
   **.storybook/preview.js**:
   ```javascript
   import '../src/app.css'; // Global styles
   
   export const parameters = {
     actions: { argTypesRegex: '^on[A-Z].*' },
     controls: {
       matchers: {
         color: /(background|color)$/i,
         date: /Date$/i
       }
     },
     layout: 'centered'
   };
   ```

3. **Project Structure**:
   ```
   src/
   ├── lib/
   │   └── components/
   │       ├── Button/
   │       │   ├── Button.svelte
   │       │   ├── Button.stories.svelte
   │       │   └── Button.test.ts
   │       └── Card/
   │           ├── Card.svelte
   │           └── Card.stories.svelte
   └── stories/
       ├── Introduction.mdx
       └── Configure.mdx
   ```

4. **Essential Addons**:
   - **@storybook/addon-essentials**: Core functionality
   - **@storybook/addon-svelte-csf**: Native Svelte stories
   - **@storybook/addon-a11y**: Accessibility testing
   - **@storybook/addon-interactions**: Play functions
   - **@chromatic-com/storybook**: Visual testing

5. **Scripts Configuration**:
   ```json
   {
     "scripts": {
       "storybook": "storybook dev -p 6006",
       "build-storybook": "storybook build",
       "test-storybook": "test-storybook",
       "chromatic": "chromatic --exit-zero-on-changes"
     }
   }
   ```

6. **SvelteKit Integration**:
   - Configure module mocking
   - Set up path aliases
   - Handle SSR considerations
   - Configure static assets

## Example Usage

User: "Set up Storybook for my new SvelteKit project"

Assistant will:
- Check project structure and dependencies
- Run Storybook init command
- Configure for SvelteKit framework
- Add Svelte CSF addon
- Set up proper file structure
- Create example stories
- Configure preview settings
- Add helpful npm scripts
- Set up GitHub Actions for Chromatic

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
