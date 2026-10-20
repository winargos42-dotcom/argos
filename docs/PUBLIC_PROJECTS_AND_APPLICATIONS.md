# ARGOS — Public projects, contests and applications registry

Updated: 2026-10-19. This is a public **link and evidence index**, not a claim that every application was accepted, funded or even submitted. Where there is no independently verified receipt, the status remains **unconfirmed**. Private correspondence, account identifiers, and application PDFs are intentionally not published.

## Published projects and verifiable public submissions

| Program / project | Public link | Status and evidence |
|---|---|---|
| PCBWay 9th Project Design Contest — Edge AI & IoT | [ARGOS-MUKHTAR project](https://www.pcbway.com/project/shareproject/ARGOS_MUKHTAR_Bio_Inspired_Edge_AI_Controller_for_a_Hexapod_4863902d.html) | **Published** 2026-10-19; public HTTP 200 and project title verified. Research prototype, no fabricated PCB claimed. |
| Hugging Face Community GPU Grant | [Application discussion #1](https://huggingface.co/spaces/AvaSiG/ARGOS-MUKHTAR-ZeroGPU/discussions/1) | **Published application** 2026-10-16; public discussion; grant award not confirmed. |
| ARGOS-MUKHTAR model/project | [HF model](https://huggingface.co/AvaSiG/ARGOS-MUKHTAR) | **Public project**, not itself proof of a contest application. |
| ARGOS-MUKHTAR Lab | [HF Space](https://huggingface.co/spaces/AvaSiG/ARGOS-MUKHTAR-Lab) | **Public project**. |
| ARGOS-MUKHTAR ZeroGPU | [HF Space](https://huggingface.co/spaces/AvaSiG/ARGOS-MUKHTAR-ZeroGPU) | **Public project**, also hosts the GPU grant discussion. |
| ARGOS-MUKHTAR BIOFUSION | [HF Space](https://huggingface.co/spaces/AvaSiG/ARGOS-MUKHTAR-BIOFUSION) | **Public project**. |
| ARGOS source | [GitHub — winargos42-dotcom/argos](https://github.com/winargos42-dotcom/argos) | **Public repository**. |
| ARGOS source | [GitHub — poilopr57-a11y/Argos](https://github.com/poilopr57-a11y/Argos) | **Project repository referenced in prior work**; current access/status not independently checked here. |

## Applications previously reported as submitted — public application page, but no public receipt link

These entries are based on earlier submission reports or correspondence, not publicly verifiable award or submission pages. Do not mistake the program homepage for an application receipt.

| Program | Public program link | Evidence status |
|---|---|---|
| Foresight Institute AI Nodes / Local Compute | [Foresight Institute](https://foresight.org/) | **SUBMITTED — saved Airtable confirmation found.** X230 evidence `grants/20261016_foresight_submission/after_submit_run9.html` contains `Thank you for submitting the form!` (SHA-256 `27bc15b96a313b6723e26efd06b03b75b541d7d11374c50441a1585e17ae77db`). Submission confirmation is not an award or payment. |
| fal Research Grants | [fal Grants](https://fal.ai/grants) | **Application email previously reported sent**; no public receipt URL. |
| LUMOS Project EDGE | [Project EDGE](https://www.lumosbot.tech/project-edge/) | **Submission previously reported**, including a form success/receipt; no public application URL. |
| Dimensional Hardware Grant | [Dimensional](https://build.dimensional.org/) | **Conflicting prior status reports** (submitted vs draft); needs receipt reconciliation. |
| Sentient Foundation Open Source AGI Grant | [Application form](https://form.typeform.com/to/IRj7WaKH) | **Conflicting prior reports** (confirmation vs 403/blocked); submission not independently verified. |
| SuperPlane OSS Sponsorship | — | **Previously reported submitted**; exact public program URL and receipt not verified. |
| Seeed Studio AI Robotics | [Seeed Studio](https://www.seeedstudio.com/) | **Outreach email previously reported sent**; not equivalent to approved grant. |
| D-Robotics | — | **Outreach previously reported**; exact URL/receipt not verified. |
| Upwork AI Agent / Azure SQL | [Upwork](https://www.upwork.com/) | **Proposal previously reported sent**; no public job/application link verified. |

## Registered, drafted, explored, or submission not confirmed

| Program | Public link | Status |
|---|---|---|
| AI Journey Contest 2026 — Coordination Referee | [Competition](https://dsworks.ru/en/champ/aij26-referee/pipeline) | **Registered and solution work underway**; a confirmed successful final submission is not established in this registry. |
| Snorkel Open Benchmarks | [Apply](https://benchmarks.snorkel.ai/apply/) | **Application prepared**; submission not confirmed. |
| T-Bank Invest Premarket | [T-Bank](https://www.tbank.ru/) | **Presentation/application planned**; submission not confirmed. |
| AMD AI Developer Program | [AMD Developer](https://www.amd.com/en/developer.html) | **Registration/credit request and appeal previously discussed**; award/credit not confirmed. |
| NLnet CodeSupply | [NLnet](https://nlnet.nl/) | **Preliminary eligibility correspondence**, not a confirmed grant application. |
| MLH Build for a Friend | [MLH](https://mlh.io/) | **Opportunity explored**; submission not confirmed. |
| Ollama and Perplexity bounties | [Ollama](https://github.com/ollama/ollama), [Perplexity](https://www.perplexity.ai/) | **Opportunities explored**; no confirmed bounty payout. |
| NEXTPCB ARGOS-MUKHTAR | [NEXTPCB](https://www.nextpcb.com/) | **Draft material exists**; submission not confirmed. |

## Maintenance rules

1. Add every new competition, grant, public demo, project, and application to this file, including the original link and a dated status.
2. Mark **submitted** only when a receipt, public submission URL, sent email record, or independently verifiable result exists; distinguish private evidence from public links.
3. Do not publish private email addresses, tokens, personal information, private application documents, or unlicensed third-party material.
4. Cross-link this registry from project READMEs and published project pages when authorized edit access exists.
5. Never imply an award, grant, or cash payment from registration or submission alone.

## MUKHTAR benchmark evidence (2026-10-20 audit)

Read-only inspection of X230 file `projects/mukhtar-runtime-stability/evidence/physical_20261016T021939Z/restart_verification.json`:

- 10 recorded attempts across 4 independent gameplay processes, one `health_gathering` map; exact live restoration passed, but OS reboot not tested.
- Before/after learning on matched seeds 63600 and 63601 (2 attempts per condition): health gain 16 -> 24; damage 100 -> 108; deaths 1 -> 1; pickups 1 -> 1.
- Report explicitly says `superiority_established=false`, `heldout_map_generalisation_proven=false`, and `native_level_exits_measured=false`. Do **not** claim proven improvement or generalization.
- These are results from October 16, not a new benchmark on October 20. Next experiment: larger matched-seed A/B with frozen vs learned checkpoints and held-out maps, with evidence and confidence intervals.

## Live verification — 2026-10-20

- X230 executed `python3 -m unittest discover -s tests -v` inside `projects/mukhtar-learning-promotion-gate`: **9/9 tests passed**.
- X230 executed `python3 learning_gate.py <restart_verification.json>` using the physical report dated October 16: **QUARANTINE**, `canary_eligible=false`, `live_promotion_performed=false`.
- The three explicit gate failures are: **2 paired seeds < 6**, **1 tested map < 2**, and **damage increased from 100 to 108**. Health gain improved 16 to 24, but this does not establish overall superiority.
- No deployment, system installation, root operation or live checkpoint promotion was performed in this audit.
- Foresight evidence files `grants/20261016_foresight_submission/after_submit_run9.html`, `run9_after_submit.png`, and `application_run9.pdf` exist locally. A saved post-submit HTML page alone is not a submission receipt; final Foresight status remains disputed pending receipt/confirmation.

## Foresight correction — 2026-10-21

The October 17 opportunities sweep's `NOT SENT` entry is contradicted by a subsequently inspected saved Airtable **post-submit success page**. The HTML has the exact text `Thank you for submitting the form!` and is paired with local before/after screenshots and a saved application PDF. Accordingly, **submission is supported by local browser evidence**, but an organizer acceptance decision, application identifier, or grant award has not been verified. Do not publish the personal application contents.
