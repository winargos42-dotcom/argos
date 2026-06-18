---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/clink/cvec/README.md
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\clink\cvec\README.md
source_ext: .md
source_sha256: 72b9a8ad41fc0d6c62ee4bb0582657bd6b57a4133a035721e8d5c4f549cd2b5e
text_sha256: 1051b3889c9d5c221bca28005d01c288295bbaa2ae3222c986effb4b25001b70
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:42
---

# README.md

- Source: `tmp/kolibrios/programs/develop/clink/cvec/README.md`
- Extract: `text`
- SHA256: `72b9a8ad41fc0d6c62ee4bb0582657bd6b57a4133a035721e8d5c4f549cd2b5e`

## Content

# cvec - partial `std::vector` implementation in C.
## Partial implementation of `std::vector`

Member functions table:

| Status | Name | Function or reason if not implemented |
| :---: | --- | --- |
| :heavy_check_mark: | `(constructor)` | `new` |
| :heavy_check_mark: | `(destructor)` | `free` |
| :heavy_check_mark: | `operator=` | `assign_other` |
| :heavy_check_mark: | `assign` | `assign_fill`, `assign_range` |
| :heavy_minus_sign: | `get_allocator` | No `allocator` objects in the language |
| :heavy_check_mark: | `at` | `at` |
| :heavy_check_mark: | `operator[]` | `[]` |
| :heavy_check_mark: | `front` | `front`, `front_p` |
| :heavy_check_mark: | `back` | `back`, `back_p` |
| :heavy_check_mark: | `data` | `data` |
| :heavy_check_mark: | `begin` | `begin` |
| :heavy_check_mark: | `cbegin` | `cbegin` |
| :heavy_check_mark: | `end` | `end` |
| :heavy_check_mark: | `cend` | `cend` |
| :heavy_minus_sign: | `rbegin` | No reverse iterators in the language |
| :heavy_minus_sign: | `crbegin` | No reverse iterators in the language |
| :heavy_minus_sign: | `rend` | No reverse iterators in the language |
| :heavy_minus_sign: | `crend` | No reverse iterators in the language |
| :heavy_check_mark: | `empty` | `empty` |
| :heavy_check_mark: | `size` | `size` |
| :heavy_check_mark: | `max_size` | `max_size` |
| :heavy_check_mark: | `reserve` | `reserve` |
| :heavy_check_mark: | `capacity` | `capacity` |
| :heavy_check_mark: | `shrink_to_fit` | `shrink_to_fit` |
| :heavy_check_mark: | `clear` | `clear` |
| :heavy_check_mark: | `insert` | `insert`, `insert_it` |
| :heavy_minus_sign: | `emplace` | I know no way to preserve the original signature |
| :heavy_check_mark: | `erase` | `erase` |
| :heavy_check_mark: | `push_back` | `push_back` |
| :heavy_minus_sign: | `emplace_back` | I know no way to preserve the original signature |
| :heavy_check_mark: | `pop_back` | `pop_back` |
| :heavy_check_mark: | `resize` | `resize` |
| :heavy_minus_sign: | `swap` | Would have n complexity in this implementation |

## Easy to use

To use the std::vector implementation for specified type they should be declared as follows:

```C
#define CVEC_TYPE TypeOfVectorElement
#include "cvec.h"

// ...

    TypeOfVectorElement *vec = cvec_TypeOfVectorElement_new(128);
    
    cvec_TypeOfVectorElement_push_back(&vec, value);
```

Also somewhere in the project the functinos should be instantiated as follows:

```C
#define CVEC_TYPE TypeOfVectorElement
#define CVEC_INST
#include "cvec.h"
```

## Allows using of custom allocators.

```C
#define CVEC_TYPE pchar
#define CVEC_INST
#define CVEC_MALLOC custom_malloc
#define CVEC_REALLOC custom_realloc
#define CVEC_FREE custom_free
#include "cvec.h"
```

## Allows handling of exceptional cases.

```C
#define CVEC_TYPE pchar
#define CVEC_INST
// Set Out Of Bounds handler
#define CVEC_OOBH(funcname, vec, index) printf("Out of bounds in %s (vec = %p, i = %d)", funcname, vec, index); abort();
#include "cvec.h"
```

## Has no fixed dependencies

Every function it uses may be overridden. More information about dependencies in [cvec.h](cvec.h).

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
