---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/ai-research/prompt-engineering-instructor/references/examples.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\ai-research\prompt-engineering-instructor\references\examples.md
source_ext: .md
source_sha256: 148791b246105e54e2cda793d52fc6dd3eebc4ddda34819d7b7b691213e089f0
text_sha256: 77da5ba3ffc15c9acd01ecd9d35090e8cdda5df7990f840024ae50d291580ea8
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:33
---

# examples.md

- Source: `claude-code-templates/cli-tool/components/skills/ai-research/prompt-engineering-instructor/references/examples.md`
- Extract: `text`
- SHA256: `148791b246105e54e2cda793d52fc6dd3eebc4ddda34819d7b7b691213e089f0`

## Content

# Real-World Examples

Practical examples of using Instructor for structured data extraction.

## Data Extraction

```python
class CompanyInfo(BaseModel):
    name: str
    founded: int
    industry: str
    employees: int

text = "Apple was founded in 1976 in the technology industry with 164,000 employees."

company = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": f"Extract: {text}"}],
    response_model=CompanyInfo
)
```

## Classification

```python
class Sentiment(str, Enum):
    POSITIVE = "positive"
    NEGATIVE = "negative"
    NEUTRAL = "neutral"

class Review(BaseModel):
    sentiment: Sentiment
    confidence: float = Field(ge=0.0, le=1.0)

review = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "This product is amazing!"}],
    response_model=Review
)
```

## Multi-Entity Extraction

```python
class Person(BaseModel):
    name: str
    role: str

class Entities(BaseModel):
    people: list[Person]
    organizations: list[str]
    locations: list[str]

entities = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Tim Cook, CEO of Apple, spoke in Cupertino..."}],
    response_model=Entities
)
```

## Structured Analysis

```python
class Analysis(BaseModel):
    summary: str
    key_points: list[str]
    sentiment: Sentiment
    actionable_items: list[str]

analysis = client.messages.create(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Analyze: [long text]"}],
    response_model=Analysis
)
```

## Batch Processing

```python
texts = ["text1", "text2", "text3"]
results = [
    client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=1024,
        messages=[{"role": "user", "content": text}],
        response_model=YourModel
    )
    for text in texts
]
```

## Streaming

```python
for partial in client.messages.create_partial(
    model="claude-sonnet-4-5-20250929",
    max_tokens=1024,
    messages=[{"role": "user", "content": "Generate report..."}],
    response_model=Report
):
    print(f"Progress: {partial.title}")
    # Update UI in real-time
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
