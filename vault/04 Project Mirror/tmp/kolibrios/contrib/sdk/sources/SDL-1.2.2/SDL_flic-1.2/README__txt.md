---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/SDL-1.2.2/SDL_flic-1.2/README.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\SDL-1.2.2\SDL_flic-1.2\README.txt
source_ext: .txt
source_sha256: e0b98466dc9aa44b3dcb9ea58b48cbd7ea5b931b5774f5dd255f222985b204bb
text_sha256: da9575ffacc247f38e6f22f005aba824deae52bf30e747849bb43371ba4641bd
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:37
---

# README.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/SDL-1.2.2/SDL_flic-1.2/README.txt`
- Extract: `text`
- SHA256: `e0b98466dc9aa44b3dcb9ea58b48cbd7ea5b931b5774f5dd255f222985b204bb`

## Content

SDL_flic version 1.2

http://www.geocities.com/andre_leiradella/

For copyright information see the source files.

SDL_flic is a small library that renders frames of FLI and FLC animation files.

The library has been tested with under Windows but should work on any platform.
The functions provided are:

. int FLI_Version(void): Returns the library version in the format
  MAJOR << 16 | MINOR.
. FLI_Animation *FLI_Open(SDL_RWops *rwops, int *error): Opens a FLIC animation
  and returns a pointer to it. rwops is left at the same point it was before
  the the call. error receives the result of the call.
. void FLI_Close(FLI_Animation *flic): Closes the animation, closes the stream
  and frees all used memory.
. int FLI_NextFrame(FLI_Animation *flic): Renders the next frame of the
  animation returning an int to indicate if it was successfull or not.
. int FLI_Rewind(FLI_Animation *flic): Rewinds the animation to the first
  frame.
. int FLI_Skip(FLI_Animation *flic): Skips the current frame without rendering
  it.

TODO:

. Handle other formats of FLIC animation.
. Play animation inside a thread?
. What else? Tell me: leiradella@bigfoot.com

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
