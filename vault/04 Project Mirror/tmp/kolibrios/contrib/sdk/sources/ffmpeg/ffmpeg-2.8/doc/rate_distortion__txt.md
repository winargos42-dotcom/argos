---
argos_import: project_file
source_path: tmp/kolibrios/contrib/sdk/sources/ffmpeg/ffmpeg-2.8/doc/rate_distortion.txt
source_abs: F:\debug\argoss\tmp\kolibrios\contrib\sdk\sources\ffmpeg\ffmpeg-2.8\doc\rate_distortion.txt
source_ext: .txt
source_sha256: 76f3cb9cbce1164e2f03ea8eca1ebf7e972cc1e4b15a98ecb90374afe8bacd64
text_sha256: 84b80cb075f9618faaadc736d43a41e7f172bd715958f2b0512482bfaa9a842f
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:29
---

# rate_distortion.txt

- Source: `tmp/kolibrios/contrib/sdk/sources/ffmpeg/ffmpeg-2.8/doc/rate_distortion.txt`
- Extract: `text`
- SHA256: `76f3cb9cbce1164e2f03ea8eca1ebf7e972cc1e4b15a98ecb90374afe8bacd64`

## Content

A Quick Description Of Rate Distortion Theory.

We want to encode a video, picture or piece of music optimally. What does
"optimally" really mean? It means that we want to get the best quality at a
given filesize OR we want to get the smallest filesize at a given quality
(in practice, these 2 goals are usually the same).

Solving this directly is not practical; trying all byte sequences 1
megabyte in length and selecting the "best looking" sequence will yield
256^1000000 cases to try.

But first, a word about quality, which is also called distortion.
Distortion can be quantified by almost any quality measurement one chooses.
Commonly, the sum of squared differences is used but more complex methods
that consider psychovisual effects can be used as well. It makes no
difference in this discussion.


First step: that rate distortion factor called lambda...
Let's consider the problem of minimizing:

  distortion + lambda*rate

rate is the filesize
distortion is the quality
lambda is a fixed value chosen as a tradeoff between quality and filesize
Is this equivalent to finding the best quality for a given max
filesize? The answer is yes. For each filesize limit there is some lambda
factor for which minimizing above will get you the best quality (using your
chosen quality measurement) at the desired (or lower) filesize.


Second step: splitting the problem.
Directly splitting the problem of finding the best quality at a given
filesize is hard because we do not know how many bits from the total
filesize should be allocated to each of the subproblems. But the formula
from above:

  distortion + lambda*rate

can be trivially split. Consider:

  (distortion0 + distortion1) + lambda*(rate0 + rate1)

This creates a problem made of 2 independent subproblems. The subproblems
might be 2 16x16 macroblocks in a frame of 32x16 size. To minimize:

  (distortion0 + distortion1) + lambda*(rate0 + rate1)

we just have to minimize:

  distortion0 + lambda*rate0

and

  distortion1 + lambda*rate1

I.e, the 2 problems can be solved independently.

Author: Michael Niedermayer
Copyright: LGPL

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
