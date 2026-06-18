---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/database/supabase-postgres-best-practices/rules/advanced-full-text-search.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\database\supabase-postgres-best-practices\rules\advanced-full-text-search.md
source_ext: .md
source_sha256: 0682b713263c5b6b9638a31f810bad07aa179bc4f79bbb787b92ed287e00fe76
text_sha256: 40c2606bbb4c4dce31308f201b24cc7f58c7df05b1d9c6856fe2b888d3b7cf28
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:35
---

# advanced-full-text-search.md

- Source: `claude-code-templates/cli-tool/components/skills/database/supabase-postgres-best-practices/rules/advanced-full-text-search.md`
- Extract: `text`
- SHA256: `0682b713263c5b6b9638a31f810bad07aa179bc4f79bbb787b92ed287e00fe76`

## Content

---
title: Use tsvector for Full-Text Search
impact: MEDIUM
impactDescription: 100x faster than LIKE, with ranking support
tags: full-text-search, tsvector, gin, search
---

## Use tsvector for Full-Text Search

LIKE with wildcards can't use indexes. Full-text search with tsvector is orders of magnitude faster.

**Incorrect (LIKE pattern matching):**

```sql
-- Cannot use index, scans all rows
select * from articles where content like '%postgresql%';

-- Case-insensitive makes it worse
select * from articles where lower(content) like '%postgresql%';
```

**Correct (full-text search with tsvector):**

```sql
-- Add tsvector column and index
alter table articles add column search_vector tsvector
  generated always as (to_tsvector('english', coalesce(title,'') || ' ' || coalesce(content,''))) stored;

create index articles_search_idx on articles using gin (search_vector);

-- Fast full-text search
select * from articles
where search_vector @@ to_tsquery('english', 'postgresql & performance');

-- With ranking
select *, ts_rank(search_vector, query) as rank
from articles, to_tsquery('english', 'postgresql') query
where search_vector @@ query
order by rank desc;
```

Search multiple terms:

```sql
-- AND: both terms required
to_tsquery('postgresql & performance')

-- OR: either term
to_tsquery('postgresql | mysql')

-- Prefix matching
to_tsquery('post:*')
```

Reference: [Full Text Search](https://supabase.com/docs/guides/database/full-text-search)

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
