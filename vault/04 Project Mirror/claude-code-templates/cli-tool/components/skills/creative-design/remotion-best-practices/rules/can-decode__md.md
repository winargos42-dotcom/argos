---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/creative-design/remotion-best-practices/rules/can-decode.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\creative-design\remotion-best-practices\rules\can-decode.md
source_ext: .md
source_sha256: 1962e0af0499bc580d30b46a0f8dc5550895298b7a98a070e8d0698a6fdb8059
text_sha256: fb3f9933e45103d72530915b72a844b3454c6acc03289db5efe8f4541b088fad
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:35
---

# can-decode.md

- Source: `claude-code-templates/cli-tool/components/skills/creative-design/remotion-best-practices/rules/can-decode.md`
- Extract: `text`
- SHA256: `1962e0af0499bc580d30b46a0f8dc5550895298b7a98a070e8d0698a6fdb8059`

## Content

---
name: can-decode
description: Check if a video can be decoded by the browser using Mediabunny
metadata:
  tags: decode, validation, video, audio, compatibility, browser
---

# Checking if a video can be decoded

Use Mediabunny to check if a video can be decoded by the browser before attempting to play it.

## The `canDecode()` function

This function can be copy-pasted into any project.

```tsx
import { Input, ALL_FORMATS, UrlSource } from "mediabunny";

export const canDecode = async (src: string) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new UrlSource(src, {
      getRetryDelay: () => null,
    }),
  });

  try {
    await input.getFormat();
  } catch {
    return false;
  }

  const videoTrack = await input.getPrimaryVideoTrack();
  if (videoTrack && !(await videoTrack.canDecode())) {
    return false;
  }

  const audioTrack = await input.getPrimaryAudioTrack();
  if (audioTrack && !(await audioTrack.canDecode())) {
    return false;
  }

  return true;
};
```

## Usage

```tsx
const src = "https://remotion.media/video.mp4";
const isDecodable = await canDecode(src);

if (isDecodable) {
  console.log("Video can be decoded");
} else {
  console.log("Video cannot be decoded by this browser");
}
```

## Using with Blob

For file uploads or drag-and-drop, use `BlobSource`:

```tsx
import { Input, ALL_FORMATS, BlobSource } from "mediabunny";

export const canDecodeBlob = async (blob: Blob) => {
  const input = new Input({
    formats: ALL_FORMATS,
    source: new BlobSource(blob),
  });

  // Same validation logic as above
};
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
