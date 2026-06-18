---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/do-storage/testing.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\cloudflare-deploy\references\do-storage\testing.md
source_ext: .md
source_sha256: ba05d776b9f7c0cbfd60ff3d6ef7dfb067f6609efcbfc2acd11d6c2307c5db95
text_sha256: 035b05fed943b2322941d7bd713d4d0e3025f2e514a3ef00642fc53509133472
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:37
---

# testing.md

- Source: `claude-code-templates/cli-tool/components/skills/development/cloudflare-deploy/references/do-storage/testing.md`
- Extract: `text`
- SHA256: `ba05d776b9f7c0cbfd60ff3d6ef7dfb067f6609efcbfc2acd11d6c2307c5db95`

## Content

# DO Storage Testing

Testing Durable Objects with storage using `vitest-pool-workers`.

## Setup

**vitest.config.ts:**
```typescript
import { defineWorkersConfig } from "@cloudflare/vitest-pool-workers/config";

export default defineWorkersConfig({
  test: {
    poolOptions: {
      workers: { wrangler: { configPath: "./wrangler.toml" } }
    }
  }
});
```

**package.json:** Add `@cloudflare/vitest-pool-workers` and `vitest` to devDependencies

## Basic Testing

```typescript
import { env, runInDurableObject } from "cloudflare:test";
import { describe, it, expect } from "vitest";

describe("Counter DO", () => {
  it("increments counter", async () => {
    const id = env.COUNTER.idFromName("test");
    const result = await runInDurableObject(env.COUNTER, id, async (instance, state) => {
      const val1 = await instance.increment();
      const val2 = await instance.increment();
      return { val1, val2 };
    });
    expect(result.val1).toBe(1);
    expect(result.val2).toBe(2);
  });
});
```

## Testing SQL Storage

```typescript
it("creates and queries users", async () => {
  const id = env.USER_MANAGER.idFromName("test");
  await runInDurableObject(env.USER_MANAGER, id, async (instance, state) => {
    await instance.createUser("alice@example.com", "Alice");
    const user = await instance.getUser("alice@example.com");
    expect(user).toEqual({ email: "alice@example.com", name: "Alice" });
  });
});

it("handles schema migrations", async () => {
  const id = env.USER_MANAGER.idFromName("migration-test");
  await runInDurableObject(env.USER_MANAGER, id, async (instance, state) => {
    const version = state.storage.sql.exec(
      "SELECT value FROM _meta WHERE key = 'schema_version'"
    ).one()?.value;
    expect(version).toBe("1");
  });
});
```

## Testing Alarms

```typescript
import { runDurableObjectAlarm } from "cloudflare:test";

it("processes batch on alarm", async () => {
  const id = env.BATCH_PROCESSOR.idFromName("test");
  
  // Add items
  await runInDurableObject(env.BATCH_PROCESSOR, id, async (instance) => {
    await instance.addItem("item1");
    await instance.addItem("item2");
  });
  
  // Trigger alarm
  await runDurableObjectAlarm(env.BATCH_PROCESSOR, id);
  
  // Verify processed
  await runInDurableObject(env.BATCH_PROCESSOR, id, async (instance, state) => {
    const count = state.storage.sql.exec(
      "SELECT COUNT(*) as count FROM processed_items"
    ).one().count;
    expect(count).toBe(2);
  });
});
```

## Testing Concurrency

```typescript
it("handles concurrent increments safely", async () => {
  const id = env.COUNTER.idFromName("concurrent-test");
  
  // Parallel increments
  const results = await Promise.all([
    runInDurableObject(env.COUNTER, id, (i) => i.increment()),
    runInDurableObject(env.COUNTER, id, (i) => i.increment()),
    runInDurableObject(env.COUNTER, id, (i) => i.increment())
  ]);
  
  // All should get unique values
  expect(new Set(results).size).toBe(3);
  expect(Math.max(...results)).toBe(3);
});
```

## Test Isolation

```typescript
// Per-test unique IDs
let testId: string;
beforeEach(() => { testId = crypto.randomUUID(); });

it("isolated test", async () => {
  const id = env.MY_DO.idFromName(testId);
  // Uses unique DO instance
});

// Cleanup pattern
it("with cleanup", async () => {
  const id = env.MY_DO.idFromName("cleanup-test");
  try {
    await runInDurableObject(env.MY_DO, id, async (instance) => {});
  } finally {
    await runInDurableObject(env.MY_DO, id, async (instance, state) => {
      await state.storage.deleteAll();
    });
  }
});
```

## Testing PITR

```typescript
it("restores from bookmark", async () => {
  const id = env.MY_DO.idFromName("pitr-test");
  
  // Create checkpoint
  const bookmark = await runInDurableObject(env.MY_DO, id, async (instance, state) => {
    await state.storage.put("value", 1);
    return await state.storage.getCurrentBookmark();
  });
  
  // Modify and restore
  await runInDurableObject(env.MY_DO, id, async (instance, state) => {
    await state.storage.put("value", 2);
    await state.storage.onNextSessionRestoreBookmark(bookmark);
    state.abort();
  });
  
  // Verify restored
  await runInDurableObject(env.MY_DO, id, async (instance, state) => {
    const value = await state.storage.get("value");
    expect(value).toBe(1);
  });
});
```

## Testing Transactions

```typescript
it("rolls back on error", async () => {
  const id = env.BANK.idFromName("transaction-test");
  
  await runInDurableObject(env.BANK, id, async (instance, state) => {
    await state.storage.put("balance", 100);
    
    await expect(
      state.storage.transaction(async () => {
        await state.storage.put("balance", 50);
        throw new Error("Cancel");
      })
    ).rejects.toThrow("Cancel");
    
    const balance = await state.storage.get("balance");
    expect(balance).toBe(100); // Rolled back
  });
});
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
