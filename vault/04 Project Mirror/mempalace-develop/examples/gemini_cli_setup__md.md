---
argos_import: project_file
source_path: mempalace-develop/examples/gemini_cli_setup.md
source_abs: F:\debug\argoss\mempalace-develop\examples\gemini_cli_setup.md
source_ext: .md
source_sha256: 3c33ff721108a8fa150fd35feb554d12a4285a09f2d5403df5181fe6fac53b1e
text_sha256: 3c33ff721108a8fa150fd35feb554d12a4285a09f2d5403df5181fe6fac53b1e
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:02
---

# gemini_cli_setup.md

- Source: `mempalace-develop/examples/gemini_cli_setup.md`
- Extract: `text`
- SHA256: `3c33ff721108a8fa150fd35feb554d12a4285a09f2d5403df5181fe6fac53b1e`

## Content

# Gemini CLI Integration Guide

This guide explains how to set up MemPalace as a permanent memory for the [Gemini CLI](https://github.com/google/gemini-cli).

## Prerequisites

- Python 3.9+
- Gemini CLI installed and configured

## 1. Installation

On many Linux systems, installing Python packages globally is restricted. We recommend using a local virtual environment within the MemPalace directory.

```bash
# Clone the repository (if you haven't already)
git clone https://github.com/MemPalace/mempalace.git
cd mempalace

# Create a virtual environment
python3 -m venv .venv

# Install dependencies and MemPalace in editable mode
.venv/bin/pip install -e .
```

## 2. Initialization

Set up your "Palace" (the database) and configure your identity.

```bash
# Initialize the palace in the current directory
.venv/bin/python3 -m mempalace init .
```

### Identity and Wings (Optional but Recommended)
You can manually define who you are and what projects you work on by creating/editing these files in `~/.mempalace/`:

- **`~/.mempalace/identity.txt`**: A plain text file describing your role and focus.
- **`~/.mempalace/wing_config.json`**: A JSON file mapping projects and name variants to "Wings".

## 3. Connect to Gemini CLI (MCP)

Register MemPalace as an MCP server so Gemini CLI can use its tools.

```bash
gemini mcp add mempalace /absolute/path/to/mempalace/.venv/bin/python3 -m mempalace.mcp_server --scope user
```
*Note: Use the absolute path to ensure it works from any directory.*

## 4. Enable Auto-Saving (Hooks)

To ensure the AI saves memories automatically when conversation history becomes too long, add a `PreCompress` hook to your Gemini CLI settings.

Edit your `~/.gemini/settings.json` and add the following:

```json
{
  "hooks": {
    "PreCompress": [
      {
        "matcher": "*",
        "hooks": [
          {
            "type": "command",
            "command": "/absolute/path/to/mempalace/hooks/mempal_precompact_hook.sh"
          }
        ]
      }
    ]
  }
}
```

Make sure the hook scripts are executable:
```bash
chmod +x hooks/*.sh
```

## 5. Usage

Once connected, Gemini CLI will automatically:
- Start the MemPalace server on launch.
- Use `mempalace_search` to find relevant past discussions.
- Use the `PreCompress` hook to save new memories before they are lost.

### Manual Mining
If you want the AI to learn from your existing code or docs immediately, run the "mine" command:
```bash
.venv/bin/python3 -m mempalace mine /path/to/your/project
```

### Verification
In a Gemini CLI session, you can run:
- `/mcp list`: Verify `mempalace` is `CONNECTED`.
- `/hooks panel`: Verify the `PreCompress` hook is active.

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
