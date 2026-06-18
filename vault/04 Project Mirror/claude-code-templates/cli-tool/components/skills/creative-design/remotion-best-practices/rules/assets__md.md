---
argos_import: project_file
source_path: claude-code-templates/cli-tool/components/skills/creative-design/remotion-best-practices/rules/assets.md
source_abs: F:\debug\argoss\claude-code-templates\cli-tool\components\skills\creative-design\remotion-best-practices\rules\assets.md
source_ext: .md
source_sha256: f550e98872e2e73bc32673d19b610df4894e00557369b3d9e1e7d3d0374c0fdd
text_sha256: 664160a48fe6ef76c9b25ea51b3796d39d371cb3632f380b014492412902ad42
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:13:35
---

# assets.md

- Source: `claude-code-templates/cli-tool/components/skills/creative-design/remotion-best-practices/rules/assets.md`
- Extract: `text`
- SHA256: `f550e98872e2e73bc32673d19b610df4894e00557369b3d9e1e7d3d0374c0fdd`

## Content

---
name: assets
description: Importing images, videos, audio, and fonts into Remotion
metadata:
  tags: assets, staticFile, images, fonts, public
---

# Importing assets in Remotion

## The public folder

Place assets in the `public/` folder at your project root.

## Using staticFile()

You MUST use `staticFile()` to reference files from the `public/` folder:

```tsx
import {Img, staticFile} from 'remotion';

export const MyComposition = () => {
  return <Img src={staticFile('logo.png')} />;
};
```

The function returns an encoded URL that works correctly when deploying to subdirectories.

## Using with components

**Images:**

```tsx
import {Img, staticFile} from 'remotion';

<Img src={staticFile('photo.png')} />;
```

**Videos:**

```tsx
import {Video} from '@remotion/media';
import {staticFile} from 'remotion';

<Video src={staticFile('clip.mp4')} />;
```

**Audio:**

```tsx
import {Audio} from '@remotion/media';
import {staticFile} from 'remotion';

<Audio src={staticFile('music.mp3')} />;
```

**Fonts:**

```tsx
import {staticFile} from 'remotion';

const fontFamily = new FontFace('MyFont', `url(${staticFile('font.woff2')})`);
await fontFamily.load();
document.fonts.add(fontFamily);
```

## Remote URLs

Remote URLs can be used directly without `staticFile()`:

```tsx
<Img src="https://example.com/image.png" />
<Video src="https://remotion.media/video.mp4" />
```

## Important notes

- Remotion components (`<Img>`, `<Video>`, `<Audio>`) ensure assets are fully loaded before rendering
- Special characters in filenames (`#`, `?`, `&`) are automatically encoded

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
