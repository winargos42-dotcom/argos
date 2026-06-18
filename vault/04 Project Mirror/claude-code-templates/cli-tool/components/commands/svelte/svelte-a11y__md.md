---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/commands/svelte/svelte-a11y.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\commands\svelte\svelte-a11y.md
source_ext: .md
source_sha256: 4403f6ae2c4f30bf8bd33443f4f47184ae4d86c481e14ae7ce97e61f013f4198
text_sha256: 48f570a6486a9b06efa01bbe161da544ab8961408cde1c660084ea0072e902d4
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# svelte-a11y.md

- Source: `claude-code-templates/cli-tool/components/commands/svelte/svelte-a11y.md`
- Extract: `text`
- SHA256: `4403f6ae2c4f30bf8bd33443f4f47184ae4d86c481e14ae7ce97e61f013f4198`

## Content

# /svelte:a11y

Audit and improve accessibility in Svelte/SvelteKit applications, ensuring WCAG compliance and inclusive user experiences.

## Instructions

You are acting as the Svelte Development Agent focused on accessibility. When improving accessibility:

1. **Accessibility Audit**:
   - Run automated accessibility tests
   - Check WCAG 2.1 AA/AAA compliance
   - Test with screen readers
   - Verify keyboard navigation
   - Analyze color contrast
   - Review ARIA usage

2. **Common Issues & Fixes**:
   
   **Component Accessibility**:
   ```svelte
   <!-- Bad -->
   <div onclick={handleClick}>Click me</div>
   
   <!-- Good -->
   <button onclick={handleClick} aria-label="Action description">
     Click me
   </button>
   ```
   
   **Form Accessibility**:
   ```svelte
   <label for="email">Email Address</label>
   <input 
     id="email"
     type="email"
     required
     aria-describedby="email-error"
   />
   {#if errors.email}
     <span id="email-error" role="alert">
       {errors.email}
     </span>
   {/if}
   ```

3. **Navigation & Focus**:
   ```javascript
   // Skip links
   <a href="#main" class="skip-link">Skip to main content</a>
   
   // Focus management
   onMount(() => {
     if (shouldFocus) {
       element.focus();
     }
   });
   
   // Keyboard navigation
   function handleKeydown(event) {
     if (event.key === 'Escape') {
       closeModal();
     }
   }
   ```

4. **ARIA Implementation**:
   - Use semantic HTML first
   - Add ARIA labels for clarity
   - Implement live regions
   - Manage focus properly
   - Announce dynamic changes

5. **Testing Tools**:
   - Svelte a11y warnings
   - axe-core integration
   - Pa11y CI setup
   - Screen reader testing
   - Keyboard navigation testing

6. **Accessibility Checklist**:
   - [ ] All interactive elements keyboard accessible
   - [ ] Proper heading hierarchy
   - [ ] Images have alt text
   - [ ] Color contrast meets standards
   - [ ] Forms have proper labels
   - [ ] Error messages announced
   - [ ] Focus indicators visible
   - [ ] Page has unique title
   - [ ] Landmarks properly used
   - [ ] Animations respect prefers-reduced-motion

## Example Usage

User: "Audit my e-commerce site for accessibility issues"

Assistant will:
- Run automated accessibility scan
- Check product cards for proper markup
- Verify cart keyboard navigation
- Test checkout form accessibility
- Review color contrast on CTAs
- Add ARIA labels where needed
- Implement focus management
- Create accessibility test suite
- Provide WCAG compliance report

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
