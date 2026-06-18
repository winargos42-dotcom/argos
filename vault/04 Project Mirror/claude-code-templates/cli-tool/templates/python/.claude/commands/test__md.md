---
argos_import: project_file
source_path: claude-code-templates/cli-tool/templates/python/.claude/commands/test.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\templates\python\.claude\commands\test.md
source_ext: .md
source_sha256: 1ff13fb7267ee38a69a7f41f8e589c8019cff254e0349aa3a7c97f9c395fd9c7
text_sha256: 17a43d1ed870b48c1dfb6ed91353fe3e45448d5d0df638662c7a96b8a69ee70d
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:54
---

# test.md

- Source: `claude-code-templates/cli-tool/templates/python/.claude/commands/test.md`
- Extract: `text`
- SHA256: `1ff13fb7267ee38a69a7f41f8e589c8019cff254e0349aa3a7c97f9c395fd9c7`

## Content

# Test Runner

Run Python tests with pytest, unittest, or other testing frameworks.

## Purpose

This command helps you run Python tests effectively with proper configuration and reporting.

## Usage

```
/test
```

## What this command does

1. **Detects test framework** (pytest, unittest, nose2)
2. **Runs appropriate tests** with proper configuration
3. **Provides coverage reporting** if available
4. **Shows clear test results** with failure details

## Example Commands

### pytest (recommended)
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src --cov-report=html

# Run specific test file
pytest tests/test_models.py

# Run with verbose output
pytest -v

# Run tests matching pattern
pytest -k "test_user"
```

### unittest
```bash
# Run all tests
python -m unittest discover

# Run specific test file
python -m unittest tests.test_models

# Run with verbose output
python -m unittest -v
```

### Django tests
```bash
# Run all Django tests
python manage.py test

# Run specific app tests
python manage.py test myapp

# Run with coverage
coverage run --source='.' manage.py test
coverage report
```

## Best Practices

- Write tests for all critical functionality
- Use descriptive test names
- Keep tests isolated and independent
- Mock external dependencies
- Aim for high test coverage (80%+)

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
