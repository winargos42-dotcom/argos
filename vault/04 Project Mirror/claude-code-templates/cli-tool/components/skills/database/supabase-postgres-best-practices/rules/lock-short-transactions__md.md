---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/database/supabase-postgres-best-practices/rules/lock-short-transactions.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\database\supabase-postgres-best-practices\rules\lock-short-transactions.md
source_ext: .md
source_sha256: 2538a22231c0dfde9967812b6bd5fb347287b671f72806495f89d0d0764e5fe6
text_sha256: 5aa7f61095916986d39644b446cdbcd2bacca7ef698a3bb50b3f82dd60207602
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:35
---

# lock-short-transactions.md

- Source: `claude-code-templates/cli-tool/components/skills/database/supabase-postgres-best-practices/rules/lock-short-transactions.md`
- Extract: `text`
- SHA256: `2538a22231c0dfde9967812b6bd5fb347287b671f72806495f89d0d0764e5fe6`

## Content

---
title: Keep Transactions Short to Reduce Lock Contention
impact: MEDIUM-HIGH
impactDescription: 3-5x throughput improvement, fewer deadlocks
tags: transactions, locking, contention, performance
---

## Keep Transactions Short to Reduce Lock Contention

Long-running transactions hold locks that block other queries. Keep transactions as short as possible.

**Incorrect (long transaction with external calls):**

```sql
begin;
select * from orders where id = 1 for update;  -- Lock acquired

-- Application makes HTTP call to payment API (2-5 seconds)
-- Other queries on this row are blocked!

update orders set status = 'paid' where id = 1;
commit;  -- Lock held for entire duration
```

**Correct (minimal transaction scope):**

```sql
-- Validate data and call APIs outside transaction
-- Application: response = await paymentAPI.charge(...)

-- Only hold lock for the actual update
begin;
update orders
set status = 'paid', payment_id = $1
where id = $2 and status = 'pending'
returning *;
commit;  -- Lock held for milliseconds
```

Use `statement_timeout` to prevent runaway transactions:

```sql
-- Abort queries running longer than 30 seconds
set statement_timeout = '30s';

-- Or per-session
set local statement_timeout = '5s';
```

Reference: [Transaction Management](https://www.postgresql.org/docs/current/tutorial-transactions.html)

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
