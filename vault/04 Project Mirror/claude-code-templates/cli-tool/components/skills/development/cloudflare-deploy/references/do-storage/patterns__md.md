---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/do-storage/patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\do-storage\patterns.md
source_ext: .md
source_sha256: 98d679c830560dce1383147eecb12404e6f69b7f5180355c59b983808d32f472
text_sha256: a60c80f45d7b13b161a93b5c14771161cf95c4876224a699ba74816207de54ea
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/do-storage/patterns.md`
- Extract: `text`
- SHA256: `98d679c830560dce1383147eecb12404e6f69b7f5180355c59b983808d32f472`

## Content

# DO Storage Patterns & Best Practices

## Schema Migration

```typescript
export class MyDurableObject extends DurableObject {
  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
    this.sql = ctx.storage.sql;
    
    // Use SQLite's built-in user_version pragma
    const ver = this.sql.exec("PRAGMA user_version").one()?.user_version || 0;
    
    if (ver === 0) {
      this.sql.exec(`CREATE TABLE users(id INTEGER PRIMARY KEY, name TEXT)`);
      this.sql.exec("PRAGMA user_version = 1");
    }
    if (ver === 1) {
      this.sql.exec(`ALTER TABLE users ADD COLUMN email TEXT`);
      this.sql.exec("PRAGMA user_version = 2");
    }
  }
}
```

## In-Memory Caching

```typescript
export class UserCache extends DurableObject {
  cache = new Map<string, User>();
  async getUser(id: string): Promise<User | undefined> {
    if (this.cache.has(id)) {
      const cached = this.cache.get(id);
      if (cached) return cached;
    }
    const user = await this.ctx.storage.get<User>(`user:${id}`);
    if (user) this.cache.set(id, user);
    return user;
  }
  async updateUser(id: string, data: Partial<User>) {
    const updated = { ...await this.getUser(id), ...data };
    this.cache.set(id, updated);
    await this.ctx.storage.put(`user:${id}`, updated);
    return updated;
  }
}
```

## Rate Limiting

```typescript
export class RateLimiter extends DurableObject {
  async checkLimit(key: string, limit: number, window: number): Promise<boolean> {
    const now = Date.now();
    this.sql.exec('DELETE FROM requests WHERE key = ? AND timestamp < ?', key, now - window);
    const count = this.sql.exec('SELECT COUNT(*) as count FROM requests WHERE key = ?', key).one().count;
    if (count >= limit) return false;
    this.sql.exec('INSERT INTO requests (key, timestamp) VALUES (?, ?)', key, now);
    return true;
  }
}
```

## Batch Processing with Alarms

```typescript
export class BatchProcessor extends DurableObject {
  pending: string[] = [];
  async addItem(item: string) {
    this.pending.push(item);
    if (!await this.ctx.storage.getAlarm()) await this.ctx.storage.setAlarm(Date.now() + 5000);
  }
  async alarm() {
    const items = [...this.pending];
    this.pending = [];
    this.sql.exec(`INSERT INTO processed_items (item, timestamp) VALUES ${items.map(() => "(?, ?)").join(", ")}`, ...items.flatMap(item => [item, Date.now()]));
  }
}
```

## Initialization Pattern

```typescript
export class Counter extends DurableObject {
  value: number;
  constructor(ctx: DurableObjectState, env: Env) {
    super(ctx, env);
    ctx.blockConcurrencyWhile(async () => { this.value = (await ctx.storage.get("value")) || 0; });
  }
  async increment() {
    this.value++;
    this.ctx.storage.put("value", this.value); // Don't await (output gate protects)
    return this.value;
  }
}
```

## Safe Counter / Optimized Write

```typescript
// Input gate blocks other requests
async getUniqueNumber(): Promise<number> {
  let val = await this.ctx.storage.get("counter");
  await this.ctx.storage.put("counter", val + 1);
  return val;
}

// No await on write - output gate delays response until write confirms
async increment(): Promise<Response> {
  let val = await this.ctx.storage.get("counter");
  this.ctx.storage.put("counter", val + 1);
  return new Response(String(val));
}
```

## Parent-Child Coordination

Hierarchical DO pattern where parent manages child DOs:

```typescript
// Parent DO coordinates children
export class Workspace extends DurableObject {
  async createDocument(name: string): Promise<string> {
    const docId = crypto.randomUUID();
    const childId = this.env.DOCUMENT.idFromName(`${this.ctx.id.toString()}:${docId}`);
    const childStub = this.env.DOCUMENT.get(childId);
    await childStub.initialize(name);
    
    // Track child in parent storage
    this.sql.exec('INSERT INTO documents (id, name, created) VALUES (?, ?, ?)', 
      docId, name, Date.now());
    return docId;
  }
  
  async listDocuments(): Promise<string[]> {
    return this.sql.exec('SELECT id FROM documents').toArray().map(r => r.id);
  }
}

// Child DO
export class Document extends DurableObject {
  async initialize(name: string) {
    this.sql.exec('CREATE TABLE IF NOT EXISTS content(key TEXT PRIMARY KEY, value TEXT)');
    this.sql.exec('INSERT INTO content VALUES (?, ?)', 'name', name);
  }
}
```

## Write Coalescing Pattern

Multiple writes to same key coalesce atomically (last write wins):

```typescript
async updateMetrics(userId: string, actions: Action[]) {
  // All writes coalesce - no await needed
  for (const action of actions) {
    this.ctx.storage.put(`user:${userId}:lastAction`, action.type);
    this.ctx.storage.put(`user:${userId}:count`, 
      await this.ctx.storage.get(`user:${userId}:count`) + 1);
  }
  // Output gate ensures all writes confirm before response
  return new Response("OK");
}

// Atomic batch with SQL
async batchUpdate(items: Item[]) {
  this.sql.exec('BEGIN');
  for (const item of items) {
    this.sql.exec('INSERT OR REPLACE INTO items VALUES (?, ?)', item.id, item.value);
  }
  this.sql.exec('COMMIT');
}
```

## Cleanup

```typescript
async cleanup() {
  await this.ctx.storage.deleteAlarm(); // Separate from deleteAll
  await this.ctx.storage.deleteAll();
}
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
