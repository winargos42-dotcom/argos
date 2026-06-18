---
argos_import: project_file
source_path: tmp/kolibrios/programs/other/fft/FHT.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\other\fft\FHT.txt
source_ext: .txt
source_sha256: 34bfa1622bf946c75171449ebc0fc3403fdf1eb345d815b9bc1ee6803185a94d
text_sha256: 696c2daf1a312a436b20010efb2ba5a0b78072711057e31baf796bdab5c698c9
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:47
---

# FHT.txt

- Source: `tmp/kolibrios/programs/other/fft/FHT.txt`
- Extract: `text`
- SHA256: `34bfa1622bf946c75171449ebc0fc3403fdf1eb345d815b9bc1ee6803185a94d`

## Content

This is a draft version of my Fast Hartley Transform (FHT) routine for KolibriOS

Hartley transform is a real-basis version of well-known Fourier transform:

1) basis function:    cas(x) = cos(x) + sin(x);
2) forward transform: H(f) = sum(k=0..N-1) [X(k)*cas(kf/(2*pi*N))] 
3) reverse transform: X(k) = 1/N * sum(f=0..N-1) [H(f)*cas(kf/(2*pi*N))] 

FHT is known to be faster than most conventional fast Fourier transform (FHT) methods.
It also uses half-length arrays due to no need of imaginary data storage.

FHT can be easily converted to FFT (and back) with no loss of information.
Most of general tasks FFT used for (correlation, convolution, energy spectra, noise
filtration, differential math, phase detection ect.) may be done directly with FHT.

====================================================================================

Copyright (C) A. Jerdev 1999, 2003 and 2010. 

The code can be used, changed and redistributed in any KolibriOS application
with only two limitations:

1) the author's name and copyright information cannot be deleted or changed;

2) the code is not allowed to be ported to or distributed with other operation systems.

18/09/2010
Artem Jerdev <kolibri@jerdev.co.uk>

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
