---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-9.2.5/src/mesa/x86-64/calling_convention.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\Mesa\mesa-9.2.5\src\mesa\x86-64\calling_convention.txt
source_ext: .txt
source_sha256: 3713b567f84e69b75cd1259041ac51c84d86b481aa915e232c8ac728de9ce5a5
text_sha256: a13560dc28a2708af8bb74a63704a7f24d1dbb5a3be9bfb746cbed3525ba80d2
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:36
---

# calling_convention.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/Mesa/mesa-9.2.5/src/mesa/x86-64/calling_convention.txt`
- Extract: `text`
- SHA256: `3713b567f84e69b75cd1259041ac51c84d86b481aa915e232c8ac728de9ce5a5`

## Content

Register Usage
rax      temporary register; with variable arguments passes information
         about the number of SSE registers used; 1st return register

rbx*     callee-saved register; optionally used as base pointer

rcx      used to pass 4th integer argument to functions

rdx      used to pass 3rd argument to functions 2nd return register

rsp*     stack pointer

rbp*     callee-saved register; optionally used as frame pointer

rsi      used to pass 2nd argument to functions

rdi      used to pass 1st argument to functions

r8       used to pass 5th argument to functions

r9       used to pass 6th argument to functions

r10      temporary register, used for passing a function's static chain pointer

r11      temporary register

r12-15*  callee-saved registers

xmm01   used to pass and return floating point arguments

xmm27   used to pass floating point arguments

xmm815  temporary registers

mmx07   temporary registers

st0      temporary register; used to return long double arguments

st1      temporary registers; used to return long double arguments

st27    temporary registers

fs       Reserved for system use (as thread specific data register)

	

*) must be preserved across function calls

Integer arguments from list: rdi,rsi,rdx,rcx,r8,r9,stack
Floating point arguments from list: xmm0-xmm7

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
