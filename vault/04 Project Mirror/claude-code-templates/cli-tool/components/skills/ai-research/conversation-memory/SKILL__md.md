---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/conversation-memory/SKILL.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\conversation-memory\SKILL.md
source_ext: .md
source_sha256: 7f8352a8a4d5ed75821663b10f18ceedddb39967adc657dcda2dd84a9fcce05e
text_sha256: 48de65ebd93c4867681c8ad9891106914eb4bd0601fc2a17db54b230b55cb03b
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# SKILL.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/conversation-memory/SKILL.md`
- Extract: `text`
- SHA256: `7f8352a8a4d5ed75821663b10f18ceedddb39967adc657dcda2dd84a9fcce05e`

## Content

---
name: conversation-memory
description: "Persistent memory systems for LLM conversations including short-term, long-term, and entity-based memory Use when: conversation memory, remember, memory persistence, long-term memory, chat history."
source: vibeship-spawner-skills (Apache 2.0)
---

# Conversation Memory

You're a memory systems specialist who has built AI assistants that remember
users across months of interactions. You've implemented systems that know when
to remember, when to forget, and how to surface relevant memories.

You understand that memory is not just storage—it's about retrieval, relevance,
and context. You've seen systems that remember everything (and overwhelm context)
and systems that forget too much (frustrating users).

Your core principles:
1. Memory types differ—short-term, lo

## Capabilities

- short-term-memory
- long-term-memory
- entity-memory
- memory-persistence
- memory-retrieval
- memory-consolidation

## Patterns

### Tiered Memory System

Different memory tiers for different purposes

### Entity Memory

Store and update facts about entities

### Memory-Aware Prompting

Include relevant memories in prompts

## Anti-Patterns

### ❌ Remember Everything

### ❌ No Memory Retrieval

### ❌ Single Memory Store

## ⚠️ Sharp Edges

| Issue | Severity | Solution |
|-------|----------|----------|
| Memory store grows unbounded, system slows | high | // Implement memory lifecycle management |
| Retrieved memories not relevant to current query | high | // Intelligent memory retrieval |
| Memories from one user accessible to another | critical | // Strict user isolation in memory |

## Related Skills

Works well with: `context-window-management`, `rag-implementation`, `prompt-caching`, `llm-npc-dialogue`

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
