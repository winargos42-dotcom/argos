---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/agents-llamaindex/references/data_connectors.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\agents-llamaindex\references\data_connectors.md
source_ext: .md
source_sha256: 3cce0923697fd88719bacd422e4a169bf67cba7352952a5d5082dab69f963567
text_sha256: 8ec7804e4e3b2c1aace849ee8ce1176ee51205b8e55507115fc16cb795db99d6
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:30
---

# data_connectors.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/agents-llamaindex/references/data_connectors.md`
- Extract: `text`
- SHA256: `3cce0923697fd88719bacd422e4a169bf67cba7352952a5d5082dab69f963567`

## Content

# LlamaIndex Data Connectors Guide

300+ data connectors via LlamaHub.

## Built-in loaders

### SimpleDirectoryReader

```python
from llama_index.core import SimpleDirectoryReader

# Load all files
documents = SimpleDirectoryReader("./data").load_data()

# Filter by extension
documents = SimpleDirectoryReader(
    "./data",
    required_exts=[".pdf", ".docx", ".txt"]
).load_data()

# Recursive
documents = SimpleDirectoryReader("./data", recursive=True).load_data()
```

### Web pages

```python
from llama_index.readers.web import SimpleWebPageReader, BeautifulSoupWebReader

# Simple loader
reader = SimpleWebPageReader()
documents = reader.load_data(["https://example.com"])

# Advanced (BeautifulSoup)
reader = BeautifulSoupWebReader()
documents = reader.load_data(urls=[
    "https://docs.python.org",
    "https://numpy.org"
])
```

### PDF

```python
from llama_index.readers.file import PDFReader

reader = PDFReader()
documents = reader.load_data("paper.pdf")
```

### GitHub

```python
from llama_index.readers.github import GithubRepositoryReader

reader = GithubRepositoryReader(
    owner="facebook",
    repo="react",
    filter_file_extensions=[".js", ".jsx"],
    verbose=True
)

documents = reader.load_data(branch="main")
```

## LlamaHub connectors

Visit https://llamahub.ai for 300+ connectors:
- Notion, Google Docs, Confluence
- Slack, Discord, Twitter
- PostgreSQL, MongoDB, MySQL
- S3, GCS, Azure Blob
- Stripe, Shopify, Salesforce

### Install from LlamaHub

```bash
pip install llama-index-readers-notion
```

```python
from llama_index.readers.notion import NotionPageReader

reader = NotionPageReader(integration_token="your-token")
documents = reader.load_data(page_ids=["page-id"])
```

## Custom loader

```python
from llama_index.core.readers.base import BaseReader
from llama_index.core import Document

class CustomReader(BaseReader):
    def load_data(self, file_path: str):
        # Your custom loading logic
        with open(file_path) as f:
            text = f.read()
        return [Document(text=text, metadata={"source": file_path})]

reader = CustomReader()
documents = reader.load_data("data.txt")
```

## Resources

- **LlamaHub**: https://llamahub.ai
- **Data Connectors Docs**: https://developers.llamaindex.ai/python/framework/modules/data_connectors/

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
