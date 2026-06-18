---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/rag-chroma/references/integration.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\rag-chroma\references\integration.md
source_ext: .md
source_sha256: e79c701b83a14bd310ff7d254525598c780aa3ef1442825de36d50a171865bdc
text_sha256: fe82af7e33a228d2d2f80c73b3e096937c3a49f873035d86d0e9e6ba6034f5fe
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# integration.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/rag-chroma/references/integration.md`
- Extract: `text`
- SHA256: `e79c701b83a14bd310ff7d254525598c780aa3ef1442825de36d50a171865bdc`

## Content

# Chroma Integration Guide

Integration with LangChain, LlamaIndex, and frameworks.

## LangChain

```python
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings

vectorstore = Chroma.from_documents(
    documents=docs,
    embedding=OpenAIEmbeddings(),
    persist_directory="./chroma_db"
)

# Query
results = vectorstore.similarity_search("query", k=3)

# As retriever
retriever = vectorstore.as_retriever()
```

## LlamaIndex

```python
from llama_index.vector_stores.chroma import ChromaVectorStore
import chromadb

db = chromadb.PersistentClient(path="./chroma_db")
collection = db.get_or_create_collection("docs")

vector_store = ChromaVectorStore(chroma_collection=collection)
```

## Resources

- **Docs**: https://docs.trychroma.com

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
