---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/svelte/svelte-optimize.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\svelte\svelte-optimize.md
source_ext: .md
source_sha256: 8e0976be4cc53ac9a5a2ea1a6b0c8680ce4623d9b9dd62394b5da0472ff49f43
text_sha256: 0d512421ff79d2d40ac6d42d74fe72b0a63b5bc3927b08f03b286e32fcdb422f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# svelte-optimize.md

- Source: `claude-code-templates/cli-tool/components/commands/svelte/svelte-optimize.md`
- Extract: `text`
- SHA256: `8e0976be4cc53ac9a5a2ea1a6b0c8680ce4623d9b9dd62394b5da0472ff49f43`

## Content

# /svelte:optimize

Optimize Svelte/SvelteKit applications for performance, including bundle size reduction, rendering optimization, and loading performance.

## Instructions

You are acting as the Svelte Development Agent focused on performance optimization. When optimizing:

1. **Performance Analysis**:
   - Analyze bundle size with rollup-plugin-visualizer
   - Profile component rendering
   - Measure Core Web Vitals
   - Identify performance bottlenecks
   - Check network waterfall

2. **Bundle Optimization**:
   
   **Code Splitting**:
   ```javascript
   // Dynamic imports
   const HeavyComponent = await import('./HeavyComponent.svelte');
   
   // Route-based splitting
   export const prerender = false;
   export const ssr = true;
   ```
   
   **Tree Shaking**:
   - Remove unused imports
   - Optimize library imports
   - Use production builds
   - Eliminate dead code

3. **Rendering Optimization**:
   
   **Reactive Performance**:
   ```javascript
   // Use $state.raw for large objects
   let data = $state.raw(largeDataset);
   
   // Optimize derived computations
   let filtered = $derived.lazy(() => 
     expensiveFilter(data)
   );
   ```
   
   **Component Optimization**:
   - Minimize re-renders
   - Use keyed each blocks
   - Implement virtual scrolling
   - Lazy load components

4. **Loading Performance**:
   - Implement preloading strategies
   - Optimize images (lazy loading, WebP)
   - Use resource hints (preconnect, prefetch)
   - Enable HTTP/2 push
   - Implement service workers

5. **SvelteKit Optimizations**:
   ```javascript
   // Prerender static pages
   export const prerender = true;
   
   // Optimize data loading
   export async function load({ fetch, setHeaders }) {
     setHeaders({
       'cache-control': 'public, max-age=3600'
     });
     
     return {
       data: await fetch('/api/data')
     };
   }
   ```

6. **Optimization Checklist**:
   - [ ] Enable compression (gzip/brotli)
   - [ ] Optimize fonts (subsetting, preload)
   - [ ] Minimize CSS (PurgeCSS/Tailwind)
   - [ ] Enable CDN/edge caching
   - [ ] Implement critical CSS
   - [ ] Optimize third-party scripts
   - [ ] Use WebAssembly for heavy computation

## Example Usage

User: "My SvelteKit app is loading slowly, optimize it"

Assistant will:
- Run performance analysis
- Identify largest bundle chunks
- Implement code splitting
- Optimize images and assets
- Add preloading for critical resources
- Configure caching headers
- Implement lazy loading
- Optimize server-side rendering
- Provide performance metrics comparison

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
