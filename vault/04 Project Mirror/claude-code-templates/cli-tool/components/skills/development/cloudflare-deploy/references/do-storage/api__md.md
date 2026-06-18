---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/do-storage/api.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\do-storage\api.md
source_ext: .md
source_sha256: ad0fa5a914c15326afdac498520c3d637bb23cba5d5c3971bb6544319178e4ef
text_sha256: d3a0957cca017ae837bcf891d34404a6faca40a9b4d9b4be26a3f6272c223622
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# api.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/do-storage/api.md`
- Extract: `text`
- SHA256: `ad0fa5a914c15326afdac498520c3d637bb23cba5d5c3971bb6544319178e4ef`

## Content

# DO Storage API Reference

## SQL API

```typescript
const cursor = this.sql.exec('SELECT * FROM users WHERE email = ?', email);
for (let row of cursor) {} // Objects: { id, name, email }
cursor.toArray(); cursor.one(); // Single row (throws if != 1)
for (let row of cursor.raw()) {} // Arrays: [1, "Alice", "..."]

// Manual iteration
const iter = cursor[Symbol.iterator]();
const first = iter.next(); // { value: {...}, done: false }

cursor.columnNames; // ["id", "name", "email"]
cursor.rowsRead; cursor.rowsWritten; // Billing

type User = { id: number; name: string; email: string };
const user = this.sql.exec<User>('...', userId).one();
```

## Sync KV API (SQLite only)

```typescript
this.ctx.storage.kv.get("counter"); // undefined if missing
this.ctx.storage.kv.put("counter", 42);
this.ctx.storage.kv.put("user", { name: "Alice", age: 30 });
this.ctx.storage.kv.delete("counter"); // true if existed

for (let [key, value] of this.ctx.storage.kv.list()) {}

// List options: start, prefix, reverse, limit
this.ctx.storage.kv.list({ start: "user:", prefix: "user:", reverse: true, limit: 100 });
```

## Async KV API (Both backends)

```typescript
await this.ctx.storage.get("key"); // Single
await this.ctx.storage.get(["key1", "key2"]); // Multiple (max 128)
await this.ctx.storage.put("key", value); // Single
await this.ctx.storage.put({ "key1": "v1", "key2": { nested: true } }); // Multiple (max 128)
await this.ctx.storage.delete("key");
await this.ctx.storage.delete(["key1", "key2"]);
await this.ctx.storage.list({ prefix: "user:", limit: 100 });

// Options: allowConcurrency, noCache, allowUnconfirmed
await this.ctx.storage.get("key", { allowConcurrency: true, noCache: true });
await this.ctx.storage.put("key", value, { allowUnconfirmed: true, noCache: true });
```

### Storage Options

| Option | Methods | Effect | Use Case |
|--------|---------|--------|----------|
| `allowConcurrency` | get, list | Skip input gate; allow concurrent requests during read | Read-heavy metrics that don't need strict consistency |
| `noCache` | get, put, list | Skip in-memory cache; always read from disk | Rarely-accessed data or testing storage directly |
| `allowUnconfirmed` | put, delete | Return before write confirms (still protected by output gate) | Non-critical writes where latency matters more than confirmation |

## Transactions

```typescript
// Sync (SQL/sync KV only)
this.ctx.storage.transactionSync(() => {
  this.sql.exec('UPDATE accounts SET balance = balance - ? WHERE id = ?', 100, 1);
  this.sql.exec('UPDATE accounts SET balance = balance + ? WHERE id = ?', 100, 2);
  return "result";
});

// Async
await this.ctx.storage.transaction(async () => {
  const value = await this.ctx.storage.get("counter");
  await this.ctx.storage.put("counter", value + 1);
  if (value > 100) this.ctx.storage.rollback(); // Explicit rollback
});
```

## Point-in-Time Recovery

```typescript
await this.ctx.storage.getCurrentBookmark();
await this.ctx.storage.getBookmarkForTime(Date.now() - 2 * 24 * 60 * 60 * 1000);
await this.ctx.storage.onNextSessionRestoreBookmark(bookmark);
this.ctx.abort(); // Restart to apply; bookmarks lexically comparable (earlier < later)
```

## Alarms

```typescript
await this.ctx.storage.setAlarm(Date.now() + 60000); // Timestamp or Date
await this.ctx.storage.getAlarm();
await this.ctx.storage.deleteAlarm();

async alarm() { await this.doScheduledWork(); }
```

## Misc

```typescript
await this.ctx.storage.deleteAll(); // Atomic for SQLite; alarm NOT included
this.ctx.storage.sql.databaseSize; // Bytes
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
