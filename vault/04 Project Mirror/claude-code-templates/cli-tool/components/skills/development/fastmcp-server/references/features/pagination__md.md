---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/fastmcp-server/references/features/pagination.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\fastmcp-server\references\features\pagination.md
source_ext: .md
source_sha256: fcb6bf40cd5858f1205786b78ce29c2ed4b69303f08f2fe84901d1739aaa74bb
text_sha256: f89996af529405d98334b9eb56307d87732ed6c8b82a081c1fe91f4b57ee8e8c
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:44
---

# pagination.md

- Source: `claude-code-templates/cli-tool/components/skills/development/fastmcp-server/references/features/pagination.md`
- Extract: `text`
- SHA256: `fcb6bf40cd5858f1205786b78ce29c2ed4b69303f08f2fe84901d1739aaa74bb`

## Content

# Pagination

> Control how servers return large lists of components to clients.

When a server exposes many tools, resources, or prompts, returning them all in a single response can be impractical. MCP supports pagination for list operations, allowing servers to return results in manageable chunks that clients can fetch incrementally.

## Server Configuration

By default, FastMCP servers return all components in a single response for backward compatibility. To enable pagination, set the `list_page_size` parameter when creating your server. This value determines the maximum number of items returned per page across all list operations.

```python
from fastmcp import FastMCP

# Enable pagination with 50 items per page
server = FastMCP("ComponentRegistry", list_page_size=50)

# Register tools (in practice, these might come from a database or config)
@server.tool
def search(query: str) -> str:
    return f"Results for: {query}"

@server.tool
def analyze(data: str) -> dict:
    return {"status": "analyzed", "data": data}

# ... many more tools, resources, prompts
```

When `list_page_size` is configured, the `tools/list`, `resources/list`, `resources/templates/list`, and `prompts/list` endpoints all paginate their responses. Each response includes a `nextCursor` field when more results exist, which clients use to fetch subsequent pages.

### Cursor Format

Cursors are opaque base64-encoded strings per the MCP specification. Clients should treat them as black boxes, passing them unchanged between requests. The cursor encodes the offset into the result set, but this is an implementation detail that may change.

## Client Behavior

The FastMCP Client handles pagination transparently. Convenience methods like `list_tools()`, `list_resources()`, `list_resource_templates()`, and `list_prompts()` automatically fetch all pages and return the complete list. Existing code continues to work without modification.

```python
from fastmcp import Client

async with Client(server) as client:
    # Returns all 200 tools, fetching pages automatically
    tools = await client.list_tools()
    print(f"Total tools: {len(tools)}")  # 200
```

### Manual Pagination

For scenarios where you want to process results incrementally (memory-constrained environments, progress reporting, or early termination), use the `_mcp` variants with explicit cursor handling.

```python
from fastmcp import Client

async with Client(server) as client:
    # Fetch first page
    result = await client.list_tools_mcp()
    print(f"Page 1: {len(result.tools)} tools")

    # Continue fetching while more pages exist
    while result.nextCursor:
        result = await client.list_tools_mcp(cursor=result.nextCursor)
        print(f"Next page: {len(result.tools)} tools")
```

The `_mcp` methods return the raw MCP protocol objects, which include both the items and the `nextCursor` for the next page. When `nextCursor` is `None`, you've reached the end of the result set.

All four list operations support manual pagination:

| Operation          | Convenience Method          | Manual Method                             |
| ------------------ | --------------------------- | ----------------------------------------- |
| Tools              | `list_tools()`              | `list_tools_mcp(cursor=...)`              |
| Resources          | `list_resources()`          | `list_resources_mcp(cursor=...)`          |
| Resource Templates | `list_resource_templates()` | `list_resource_templates_mcp(cursor=...)` |
| Prompts            | `list_prompts()`            | `list_prompts_mcp(cursor=...)`            |

## When to Use Pagination

Pagination becomes valuable when your server exposes a large number of components. Consider enabling it when:

* Your server dynamically generates many components (e.g., from a database or file system)
* Memory usage is a concern for clients
* You want to reduce initial response latency

For servers with a fixed, modest number of components (fewer than 100), pagination adds complexity without meaningful benefit. The default behavior of returning everything in one response is simpler and efficient for typical use cases.

> ## Documentation Index
> Fetch the complete documentation index at: https://gofastmcp.com/llms.txt
> Use this file to discover all available pages before exploring further.

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
