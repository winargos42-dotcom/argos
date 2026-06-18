---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/agents-llamaindex/references/agents.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\agents-llamaindex\references\agents.md
source_ext: .md
source_sha256: 11e885ae23eedb48c9b035cf8d45b9f8bb97c95f9f47c37a6c15235440e00016
text_sha256: 755be6104ccb5acce5b61efe1753d6380a8fbeef136fa1381fa4325c6d6cb15a
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# agents.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/agents-llamaindex/references/agents.md`
- Extract: `text`
- SHA256: `11e885ae23eedb48c9b035cf8d45b9f8bb97c95f9f47c37a6c15235440e00016`

## Content

# LlamaIndex Agents Guide

Building agents with tools and RAG capabilities.

## Basic agent

```python
from llama_index.core.agent import FunctionAgent
from llama_index.llms.openai import OpenAI

def multiply(a: int, b: int) -> int:
    """Multiply two numbers."""
    return a * b

llm = OpenAI(model="gpt-4o")
agent = FunctionAgent.from_tools(
    tools=[multiply],
    llm=llm,
    verbose=True
)

response = agent.chat("What is 25 * 17?")
```

## RAG agent

```python
from llama_index.core.tools import QueryEngineTool

# Create query engine as tool
index = VectorStoreIndex.from_documents(documents)

query_tool = QueryEngineTool.from_defaults(
    query_engine=index.as_query_engine(),
    name="python_docs",
    description="Useful for Python programming questions"
)

# Agent with RAG + calculator
agent = FunctionAgent.from_tools(
    tools=[query_tool, multiply],
    llm=llm
)

response = agent.chat("According to the docs, what is Python?")
```

## Multi-document agent

```python
# Multiple knowledge bases
python_tool = QueryEngineTool.from_defaults(
    query_engine=python_index.as_query_engine(),
    name="python_docs",
    description="Python programming documentation"
)

numpy_tool = QueryEngineTool.from_defaults(
    query_engine=numpy_index.as_query_engine(),
    name="numpy_docs",
    description="NumPy array documentation"
)

agent = FunctionAgent.from_tools(
    tools=[python_tool, numpy_tool],
    llm=llm
)

# Agent chooses correct knowledge base
response = agent.chat("How do I create numpy arrays?")
```

## Best practices

1. **Clear tool descriptions** - Agent needs to know when to use each tool
2. **Limit tools to 5-10** - Too many confuses agent
3. **Use verbose mode during dev** - See agent reasoning
4. **Combine RAG + calculation** - Powerful combination
5. **Test tool combinations** - Ensure they work together

## Resources

- **Agents Docs**: https://developers.llamaindex.ai/python/framework/modules/agents/

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
