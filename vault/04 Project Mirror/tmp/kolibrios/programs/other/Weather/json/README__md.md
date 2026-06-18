---
argos_import: project_file
source_path: tmp/kolibrios/programs/other/Weather/json/README.md
source_abs: F:\debug\argoss\tmp\kolibrios\programs\other\Weather\json\README.md
source_ext: .md
source_sha256: 9f16385b01cc97c289246bb49d03c0160e0d7b539e3c35d08f9b667adaaa1ca0
text_sha256: 72a3921c70cad0d2e07ba6edbcafe65bf7cdd30a988aea7dc3afb00daf534e09
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:47
---

# README.md

- Source: `tmp/kolibrios/programs/other/Weather/json/README.md`
- Extract: `text`
- SHA256: `9f16385b01cc97c289246bb49d03c0160e0d7b539e3c35d08f9b667adaaa1ca0`

## Content

Very low footprint JSON parser written in portable ANSI C.

* BSD licensed with no dependencies (i.e. just drop the C file into your project)
* Never recurses or allocates more memory than it needs
* Very simple API with operator sugar for C++

[![Build Status](https://secure.travis-ci.org/udp/json-parser.png)](http://travis-ci.org/udp/json-parser)

_Want to serialize?  Check out [json-builder](https://github.com/udp/json-builder)!_

Installing
----------

There is now a makefile which will produce a libjsonparser static and dynamic library.  However, this
is _not_ required to build json-parser, and the source files (`json.c` and `json.h`) should be happy
in any build system you already have in place.


API
---

    json_value * json_parse (const json_char * json,
                             size_t length);

    json_value * json_parse_ex (json_settings * settings,
                                const json_char * json,
                                size_t length,
                                char * error);

    void json_value_free (json_value *);

The `type` field of `json_value` is one of:

* `json_object` (see `u.object.length`, `u.object.values[x].name`, `u.object.values[x].value`)
* `json_array` (see `u.array.length`, `u.array.values`)
* `json_integer` (see `u.integer`)
* `json_double` (see `u.dbl`)
* `json_string` (see `u.string.ptr`, `u.string.length`)
* `json_boolean` (see `u.boolean`)
* `json_null`


Compile-Time Options
--------------------

    -DJSON_TRACK_SOURCE

Stores the source location (line and column number) inside each `json_value`.

This is useful for application-level error reporting.


Runtime Options
---------------

    settings |= json_enable_comments;

Enables C-style `// line` and `/* block */` comments.

    size_t value_extra

The amount of space (if any) to allocate at the end of each `json_value`, in
order to give the application space to add metadata.

    void * (* mem_alloc) (size_t, int zero, void * user_data);
    void (* mem_free) (void *, void * user_data);

Custom allocator routines.  If NULL, the default `malloc` and `free` will be used.

The `user_data` pointer will be forwarded from `json_settings` to allow application
context to be passed.


Changes in version 1.1.0
------------------------

* UTF-8 byte order marks are now skipped if present

* Allows cross-compilation by honoring --host if given (@wkz)

* Maximum size for error buffer is now exposed in header (@LB--)

* GCC warning for `static` after `const` fixed (@batrick)

* Optional support for C-style line and block comments added (@Jin-W-FS)

* `name_length` field added to object values 

* It is now possible to retrieve the source line/column number of a parsed `json_value` when `JSON_TRACK_SOURCE` is enabled

* The application may now extend `json_value` using the `value_extra` setting

* Un-ambiguate pow call in the case of C++ overloaded pow (@fcartegnie)

* Fix null pointer de-reference when a non-existing array is closed and no root value is present

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
