---
argos_import: project_file
source_path: tmp/kolibrios/programs/games/pig/dirtyrects.txt
source_abs: F:\debug\argoss\tmp\kolibrios\programs\games\pig\dirtyrects.txt
source_ext: .txt
source_sha256: 9eae6eef1246ba99168f169947dfd34d5b10a1d07d5f0cf3b5bf32654a2c82c3
text_sha256: b0369b28908bb017c5c0630068a90c4909e64a26cfeddd4ef8774d57920f4c96
extract_mode: text
project_root: F:\debug\argoss
imported_at: 2026-05-04 04:14:46
---

# dirtyrects.txt

- Source: `tmp/kolibrios/programs/games/pig/dirtyrects.txt`
- Extract: `text`
- SHA256: `9eae6eef1246ba99168f169947dfd34d5b10a1d07d5f0cf3b5bf32654a2c82c3`

## Content

Smart Dirty Rectangle Management
	--------------------------------

pig_dirty() contains an algorithm that tries to find
the the best dirtyrect candidates for merging. While
searching, it looks out for perfect or sufficiently
good candidates.

(Perfect candidate:)
	The merged rectangle is of the same size
	as the largest of the two input rectangles:

		Amerged <= MAX(A1, A2)

  We don't actually test for this, but rather for...

Instant Pick candidate:
	Not Perfect, but good enough to be treated
	as such, considering the cost of going on
	searching for a better candidate:
		Amerged 100 / MAX(A1, A2) - 100 <= PIG_INSTANT_MERGE

	(That is, the area of the merged rect must be
	no more than PIG_INSTANT_MERGE % bigger than
	the area of the larger of the two input rects.)

	Note that this is also about how likely it is
	that thereis* a better candidate. Assuming
	that PIG_INSTANT_MERGE is set to a sensible
	value, it is not very likely at all. There
	would have to be another dirtyrect nearby, and
	the chance of that being a better match is
	rather low, since that would most likely have
	caused it to be merged with the tested dirtyrect
	long before our new rect came in.

(Good candidate:)
	The area of the merged rectangle is smaller
	than the total area of the two input rectangles:

		(Amerged - A1 - A2) < 0

  We don't actually test for this, but rather for...

Acceptable candidate:
	The area of the merged rectangle is larger
	than the total of the two input rectangles, but
	since there is some per-rectangle overhead,
	merging is still a win:

		(Amerged - A1 - A2) <= PIG_WORST_MERGE

	The default setting assumes that the cost of a
	rectangle is in the range of 300 pixels. One
	should probably benchmark a few different systems
	to see if that's reasonable.

Unacceptable candidate:
	The area of the merged rectangle is larger than
	the total of the input rectangles to the degree
	that merging is a definite loss:

		(Amerged - A1 - A2) > PIG_WORST_MERGE

The algorithm instantly returns Perfect candidates as
solutions. If there are only Good and Acceptable
candidates, the best one (lowest number of wasted
pixels) is the solution.

If there are only Unacceptable candidates, there is no
sensible merger solution, so pig_dirty() will try to add
a new dirtyrect.

If that fails (table full), the best candidate is used,
even though it would have been Unacceptable under normal
circumstances.


TODO: Thereare* more alternatives than just "merge" or
TODO: "don't merge"! For example, it might pay off to
TODO: detect overlapping and clip dirtyrects to avoid
TODO: it, when merging is not a viable option.

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
