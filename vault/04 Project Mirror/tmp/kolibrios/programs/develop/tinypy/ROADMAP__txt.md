---
argos_import: project_file
source_path: tmp/kolibrios/programs/develop/tinypy/ROADMAP.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\develop\tinypy\ROADMAP.txt
source_ext: .txt
source_sha256: 1bcb018789277f6b0a5e31194b9d50beb456fb519bbc2a98f4655e575c1b8818
text_sha256: 1a539d74970f2190f6be5295b9097be47dd1c7773e1205efe096f2b0e2980801
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:45
---

# ROADMAP.txt

- Source: `tmp/kolibrios/programs/develop/tinypy/ROADMAP.txt`
- Extract: `text`
- SHA256: `1bcb018789277f6b0a5e31194b9d50beb456fb519bbc2a98f4655e575c1b8818`

## Content

tinypy is a minimalist implementation of python in 64k of code

"batteries not included (yet)"
"lua for people who like python"

what tinypy is:
    * parser and bytecode compiler written in tinypy
    * fully bootstrapped
    * luaesque virtual machine with garbage collection written in C
      it's "stackless" sans any "stackless" features
    * cross-platform :) it runs under windows / linux / macosx
    * a fairly decent subset of python
          o classes and single inheritance
          o functions with variable or keyword arguments
          o strings, lists, dicts, numbers
          o modules, list comprehensions
          o exceptions with full traceback
          o some builtins
    - an easy C-API for building modules
    - 64k of code (for at least some definition of 64k)
    - interesting, educational, nifty, and useful
    - well tested
    - easy to read, maintain, and use
    - fun fun fun!!!
    - you can static compile it and its modules (MIT license, so "it's all good!")

what tinypy will be:
    - sandboxed
    - a Cpython module (setup.py install)
    - including some batteries (math, random, re, marshal, pygame?!)
    - Visual Studio compatible
    - documented

what tinypy might be:
    - as fast as python (maybe faster?)
    - including a JIT module
    - C89 compatible
    - C++ compatible (like lua)
    - a shed-skin module
    - including a dynamic loading module

what tinypy won't be:
    - a full implementation of python
    - totally compatible with python

alternatives to tinypy:
    - lua
    - shed-skin
    - pymite
    - pyvm
    - cython
    - pypy
    - jython
    - ironpython
    - python

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
