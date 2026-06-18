---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/prompt-engineering-instructor/references/providers.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\prompt-engineering-instructor\references\providers.md
source_ext: .md
source_sha256: 2adb6aaa74c6772dd41b19f2bdb80e1d4064d3acc6f53f0aea131c06a7da8848
text_sha256: 5482459ae8d27494b6848b9bbf4fac8c55f810bc7829ec29368ba15e5e67db6e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# providers.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/prompt-engineering-instructor/references/providers.md`
- Extract: `text`
- SHA256: `2adb6aaa74c6772dd41b19f2bdb80e1d4064d3acc6f53f0aea131c06a7da8848`

## Content

# Provider Configuration

Guide to using Instructor with different LLM providers.

## Anthropic Claude

```python
import instructor
from anthropic import Anthropic

# Basic setup
client = instructor.from_anthropic(Anthropic())

# With API key
client = instructor.from_anthropic(
    Anthropic(api_key="your-api-key")
)

# Recommended mode
client = instructor.from_anthropic(
    Anthropic(),
    mode=instructor.Mode.ANTHROPIC_TOOLS
)

# Usage
result = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "..."}],
    response_model=YourModel
)
```

## OpenAI

```python
from openai import OpenAI

client = instructor.from_openai(OpenAI())

result = client.chat.completions.create(
    model="gpt-4o-mini",
    response_model=YourModel,
    messages=[{"role": "user", "content": "..."}]
)
```

## Local Models (Ollama)

```python
client = instructor.from_openai(
    OpenAI(
        base_url="http://localhost:11434/v1",
        api_key="ollama"
    ),
    mode=instructor.Mode.JSON
)

result = client.chat.completions.create(
    model="llama3.1",
    response_model=YourModel,
    messages=[...]
)
```

## Modes

- `Mode.ANTHROPIC_TOOLS`: Recommended for Claude
- `Mode.TOOLS`: OpenAI function calling
- `Mode.JSON`: Fallback for unsupported providers

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
