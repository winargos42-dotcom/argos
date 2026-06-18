---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/email-workers/gotchas.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\email-workers\gotchas.md
source_ext: .md
source_sha256: 8599e5772e711a308a2a62cdd24a93e7bed7a8b2bda624ddd58f0d5743dacbbf
text_sha256: 135434634be61d82d5567dc20e779e9a807693d9d83ba2a49184d62ec551cb76
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# gotchas.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/email-workers/gotchas.md`
- Extract: `text`
- SHA256: `8599e5772e711a308a2a62cdd24a93e7bed7a8b2bda624ddd58f0d5743dacbbf`

## Content

# Email Workers Gotchas

## Critical Issues

### ReadableStream Single-Use

```typescript
// ❌ WRONG: Stream consumed twice
const email = await PostalMime.parse(await new Response(message.raw).arrayBuffer());
const rawText = await new Response(message.raw).text(); // EMPTY!

// ✅ CORRECT: Buffer first
const buffer = await new Response(message.raw).arrayBuffer();
const email = await PostalMime.parse(buffer);
const rawText = new TextDecoder().decode(buffer);
```

### ctx.waitUntil() Errors Silent

```typescript
// ❌ Errors dropped silently
ctx.waitUntil(fetch(webhookUrl, { method: 'POST', body: data }));

// ✅ Catch and log
ctx.waitUntil(
  fetch(webhookUrl, { method: 'POST', body: data })
    .catch(err => env.ERROR_LOG.put(`error:${Date.now()}`, err.message))
);
```

## Security

### Envelope vs Header From (Spoofing)

```typescript
const envelopeFrom = message.from;               // SMTP MAIL FROM (trusted)
const headerFrom = (await PostalMime.parse(buffer)).from?.address; // (untrusted)
// Use envelope for security decisions
```

### Input Validation

```typescript
if (message.rawSize > 5_000_000) { message.setReject('Too large'); return; }
if ((message.headers.get('Subject') || '').length > 1000) {
  message.setReject('Invalid subject'); return;
}
```

### DMARC for Replies

Replies fail silently without DMARC. Verify: `dig TXT _dmarc.example.com`

## Parsing

### Address Parsing

```typescript
const email = await PostalMime.parse(buffer);
const fromAddress = email.from?.address || 'unknown';
const toAddresses = Array.isArray(email.to) ? email.to.map(t => t.address) : [email.to?.address];
```

### Character Encoding

Let postal-mime handle decoding - `email.subject`, `email.text`, `email.html` are UTF-8.

## API Behavior

### setReject() vs throw

```typescript
// setReject() for SMTP rejection
if (blockList.includes(message.from)) { message.setReject('Blocked'); return; }

// throw for worker errors
if (!env.KV) throw new Error('KV not configured');
```

### forward() Only X-* Headers

```typescript
headers.set('X-Processed-By', 'worker');  // ✅ Works
headers.set('Subject', 'Modified');        // ❌ Dropped
```

### Reply Requires Verified Domain

```typescript
// Use same domain as receiving address
const receivingDomain = message.to.split('@')[1];
await message.reply(new EmailMessage(`noreply@${receivingDomain}`, message.from, rawMime));
```

## Performance

### CPU Limit

```typescript
// Skip parsing large emails
if (message.rawSize > 5_000_000) {
  await message.forward('inbox@example.com');
  return;
}
```

Monitor: `npx wrangler tail`

## Limits

| Limit | Value |
|-------|-------|
| Max message size | 25 MiB |
| Max rules/zone | 200 |
| CPU time (free/paid) | 10ms / 50ms |
| Reply References | 100 |

## Common Errors

| Error | Fix |
|-------|-----|
| "Address not verified" | Add in Email Routing dashboard |
| "Exceeded CPU time" | Use `ctx.waitUntil()` or upgrade |
| "Stream is locked" | Buffer `message.raw` first |
| Silent reply failure | Check DMARC records |

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
