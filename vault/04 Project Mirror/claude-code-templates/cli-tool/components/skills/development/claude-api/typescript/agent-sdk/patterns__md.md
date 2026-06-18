---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/development/claude-api/typescript/agent-sdk/patterns.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\development\claude-api\typescript\agent-sdk\patterns.md
source_ext: .md
source_sha256: dcea231dda2d20f7c6aa91d3d5dfd6ac4f0b6d0301d00884e840502eb5eb42f0
text_sha256: 8a47275106399f7274ff5db2978a8ea7addb1ac5d81086abebd42a5a620c7619
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:36
---

# patterns.md

- Source: `claude-code-templates/cli-tool/components/skills/development/claude-api/typescript/agent-sdk/patterns.md`
- Extract: `text`
- SHA256: `dcea231dda2d20f7c6aa91d3d5dfd6ac4f0b6d0301d00884e840502eb5eb42f0`

## Content

# Agent SDK Patterns — TypeScript

## Basic Agent

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

async function main() {
  for await (const message of query({
    prompt: "Explain what this repository does",
    options: {
      cwd: "/path/to/project",
      allowedTools: ["Read", "Glob", "Grep"],
    },
  })) {
    if ("result" in message) {
      console.log(message.result);
    }
  }
}

main();
```

---

## Hooks

### After Tool Use Hook

```typescript
import { query, HookCallback } from "@anthropic-ai/claude-agent-sdk";
import { appendFileSync } from "fs";

const logFileChange: HookCallback = async (input) => {
  const filePath = (input as any).tool_input?.file_path ?? "unknown";
  appendFileSync(
    "./audit.log",
    `${new Date().toISOString()}: modified ${filePath}\n`,
  );
  return {};
};

for await (const message of query({
  prompt: "Refactor utils.py to improve readability",
  options: {
    allowedTools: ["Read", "Edit", "Write"],
    permissionMode: "acceptEdits",
    hooks: {
      PostToolUse: [{ matcher: "Edit|Write", hooks: [logFileChange] }],
    },
  },
})) {
  if ("result" in message) console.log(message.result);
}
```

---

## Subagents

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Use the code-reviewer agent to review this codebase",
  options: {
    allowedTools: ["Read", "Glob", "Grep", "Agent"],
    agents: {
      "code-reviewer": {
        description: "Expert code reviewer for quality and security reviews.",
        prompt: "Analyze code quality and suggest improvements.",
        tools: ["Read", "Glob", "Grep"],
      },
    },
  },
})) {
  if ("result" in message) console.log(message.result);
}
```

---

## MCP Server Integration

### Browser Automation (Playwright)

```typescript
for await (const message of query({
  prompt: "Open example.com and describe what you see",
  options: {
    mcpServers: {
      playwright: { command: "npx", args: ["@playwright/mcp@latest"] },
    },
  },
})) {
  if ("result" in message) console.log(message.result);
}
```

---

## Session Resumption

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

let sessionId: string | undefined;

// First query: capture the session ID
for await (const message of query({
  prompt: "Read the authentication module",
  options: { allowedTools: ["Read", "Glob"] },
})) {
  if (message.type === "system" && message.subtype === "init") {
    sessionId = message.session_id;
  }
}

// Resume with full context from the first query
for await (const message of query({
  prompt: "Now find all places that call it",
  options: { resume: sessionId },
})) {
  if ("result" in message) console.log(message.result);
}
```

---

## Session History

```typescript
import { listSessions, getSessionMessages, getSessionInfo } from "@anthropic-ai/claude-agent-sdk";

async function main() {
  // List past sessions (supports pagination via limit/offset)
  const sessions = await listSessions();
  for (const session of sessions) {
    console.log(`Session ${session.sessionId} in ${session.cwd} (tag: ${session.tag})`);
  }

  // Get metadata for a single session
  if (sessions.length > 0) {
    const info = await getSessionInfo(sessions[0].sessionId);
    console.log(`Created: ${info.createdAt}, Tag: ${info.tag}`);
  }

  // Retrieve messages from the most recent session
  if (sessions.length > 0) {
    const messages = await getSessionMessages(sessions[0].sessionId, { limit: 50 });
    for (const msg of messages) {
      console.log(msg);
    }
  }
}

main();
```

---

## Session Mutations

```typescript
import { renameSession, tagSession, forkSession } from "@anthropic-ai/claude-agent-sdk";

async function main() {
  const sessionId = "your-session-id";

  // Rename a session
  await renameSession(sessionId, "Refactoring auth module");

  // Tag a session for filtering
  await tagSession(sessionId, "experiment-v2");

  // Clear a tag
  await tagSession(sessionId, null);

  // Fork a conversation to branch from a point
  const { sessionId: forkedId } = await forkSession(sessionId);
  console.log(`Forked session: ${forkedId}`);
}

main();
```

---

## Custom System Prompt

```typescript
import { query } from "@anthropic-ai/claude-agent-sdk";

for await (const message of query({
  prompt: "Review this code",
  options: {
    allowedTools: ["Read", "Glob", "Grep"],
    systemPrompt: `You are a senior code reviewer focused on:
1. Security vulnerabilities
2. Performance issues
3. Code maintainability

Always provide specific line numbers and suggestions for improvement.`,
  },
})) {
  if ("result" in message) console.log(message.result);
}
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
