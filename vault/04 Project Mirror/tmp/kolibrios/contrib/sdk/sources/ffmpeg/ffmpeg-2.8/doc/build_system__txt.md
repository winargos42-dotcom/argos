---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/ffmpeg/ffmpeg-2.8/doc/build_system.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\ffmpeg\ffmpeg-2.8\doc\build_system.txt
source_ext: .txt
source_sha256: 1361b92d066033e95441caf7d3153dfcad1d56a30bfb42f33bd793b7caf442b9
text_sha256: 1e1f48aff54d33a207ce1e151c653791409975d9fdf2c07ab5994accf19db45f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:29
---

# build_system.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/ffmpeg/ffmpeg-2.8/doc/build_system.txt`
- Extract: `text`
- SHA256: `1361b92d066033e95441caf7d3153dfcad1d56a30bfb42f33bd793b7caf442b9`

## Content

FFmpeg currently uses a custom build system, this text attempts to document
some of its obscure features and options.

Makefile variables:

V
    Disable the default terse mode, the full command issued by make and its
    output will be shown on the screen.

DBG
    Preprocess x86 external assembler files to a .dbg.asm file in the object
    directory, which then gets compiled. Helps developping those assembler
    files.

DESTDIR
    Destination directory for the install targets, useful to prepare packages
    or install FFmpeg in cross-environments.

GEN
    Set to ‘1’ to generate the missing or mismatched references.

Makefile targets:

all
    Default target, builds all the libraries and the executables.

fate
    Run the fate test suite, note you must have installed it

fate-list
    Will list all fate/regression test targets

install
    Install headers, libraries and programs.

examples
    Build all examples located in doc/examples.

libavformat/output-example
    Build the libavformat basic example.

libavcodec/api-example
    Build the libavcodec basic example.

libswscale/swscale-test
    Build the swscale self-test (useful also as example).

config
    Reconfigure the project with current configuration.


Useful standard make commands:
make -t <target>
    Touch all files that otherwise would be build, this is useful to reduce
    unneeded rebuilding when changing headers, but note you must force rebuilds
    of files that actually need it by hand then.

make -j<num>
    rebuild with multiple jobs at the same time. Faster on multi processor systems

make -k
    continue build in case of errors, this is useful for the regression tests
    sometimes but note it will still not run all reg tests.

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
