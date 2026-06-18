---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/libraries/kos_mbedtls/notes.md
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\libraries\kos_mbedtls\notes.md
source_ext: .md
source_sha256: 3db8e2084aec966619b170fa006897b0863442b6ebc485a7759c66de6b3dc234
text_sha256: 4cd75a455225f5306e00ca2ee71a1dbbac896d85f1e5fba2888bc8368fc88c36
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:43
---

# notes.md

- Source: `tmp/kolibrios/programs/develop/libraries/kos_mbedtls/notes.md`
- Extract: `text`
- SHA256: `3db8e2084aec966619b170fa006897b0863442b6ebc485a7759c66de6b3dc234`

## Content

##### Notes

- in include/mbedtls/config.h
    - uncommented:\
              MBEDTLS_NO_DEFAULT_ENTROPY_SOURCES\
              MBEDTLS_NO_PLATFORM_ENTROPY
    - commented out:\
              MBEDTLS_TIMING_C\
              MBEDTLS_FS_IO

- following functions deleted because they are NOT neccesary for programs/ssl_client1.c
    - mbedtls_net_bind
    - mbedtls_net_accept
    - mbedtls_net_poll
    - mbedtls_net_set_block
    - mbedtls_net_set_nonblock
    - mbedtls_net_usleep
    - mbedtls_net_recv_timeout


##### Other:
- Order in which you list libs in ldflags matter !

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
