# ARGOS-MUKHTAR — Independent Research Technical Profile (2026)

**Applicant:** Vsevolod Aryatikov (Всеволод Арятиков)  
**Location:** Komsomolsk-on-Amur, Russian Federation  
**Contact:** winargos42@gmail.com  
**Status:** Independent individual researcher and developer, not a university, company, or incorporated laboratory  
**Project home:** [ARGOS Universal OS](https://github.com/winargos42-dotcom/argos)  
**Purpose of this document:** Public technical CV / project profile for research partners and Foresight Institute's 2026 *AI for Safety & Science Nodes* RFP. Updated 27 October 2026.

## Research objective

ARGOS-MUKHTAR is an exploratory, **local-first, resource-constrained embodied AI research project** combining insect-inspired neural processing, learning and memory, autonomous agent orchestration, and edge inference. The goal is to make experiments on perception, action, adaptation, and safety **measurable and reproducible on modest, personally operated hardware**.

The aim is **not** to claim a completed whole-brain emulation or human-level intelligence. We seek hardware, time, and community review to turn working prototypes into public, scientifically useful experiments.

## Existing engineering foundation

The broader ARGOS Universal OS platform provides a Linux/Docker-based orchestration environment with agent tools, local model serving, telemetry, long-term memory components, and test automation. The research stack has been exercised across an older ThinkPad workstation and a dedicated Linux node.

The project's hardware research includes:

- **Google Coral Edge TPU:** temporal INT8 BioLocator/Student control experiments. Previous local logs recorded approximately **0.245–0.283 ms per inference** under their particular test conditions. These are preliminary hardware measurements, not general throughput benchmarks.
- **GTI2801 inference hardware:** four addressable device channels have been observed at `/dev/gti2800-0..3` with GTI SDK 4.5.1. A factory-model visual frontend produced spatial outputs in approximately **13–14 ms** under local tests.
- **FPGA/PCIe experiments:** an Xilinx Artix-7-based SPR2801S board and custom integration work. Driver, DMA stability, and original vendor toolchain/licensing remain limitations.
- **Biomimetic motor control:** a LIF/CPG-style loop with 2 ms simulation/control steps (500 Hz), safety gating, and a research interface to MuJoCo/ViZDoom.
- **MaleCNS-derived data:** the research design references a Drosophila connectome with **167,565 neurons and approximately 25.6 million synapses**. Use of these data does **not** mean that all 167,565 neurons have been run in one validated, closed-loop hardware simulation.

## Experimental observations (internal, not independently replicated)

- The BioLocator v2/v3 line was evaluated on held-out navigation/bearing tasks; local notes report positive controlled results. Dataset splits and full scripts need public release before scientific claims can be independently verified.
- A ViZDoom causal comparison at a selected evaluation checkpoint reported agent health values of **58 with the memory-enabled condition, 40 without memory, and 28 with shuffled mapping**. This is an **exploratory observation**, not a statistically powered benchmark or proof of generalized learning.
- Two simultaneous GTI2801 streams have been reported stable in a narrow test; aggressive four-way use has triggered DMA timeouts. **Stability under load is an open engineering risk.**
- Custom FC-head adaptation using features produced by a factory GTI model was tested. This **does not** establish that arbitrary custom convolutional networks can be compiled and deployed to the GTI2801 silicon.

The project distinguishes **measured observations**, **local unreviewed results**, and **future research objectives**. Individual numbers should not be read as externally audited performance claims.

## Proposed 12-month research program

**Work package 1 — Reproducible local compute node (months 1–3).** Stabilize compute, storage, power, workload isolation and logging; archive datasets and software environments; automate deterministic A/B test runs.

**Work package 2 — Quantitative benchmark design (months 3–6).** Release control baselines, frozen models, memory ablations, and mirrored/chirality-balanced evaluations; measure success, survival, inference latency, resource use, and hardware failure rates across randomized seeds.

**Work package 3 — Embodied adaptation (months 6–9).** Connect neural and learning components to safe simulated insect/hexapod control; test transfer from ViZDoom or 2D scenes to physics-based robotics; document when adaptation fails.

**Work package 4 — Reproduction and public outputs (months 9–12).** Publish benchmark scripts, anonymized experiment logs, hardware-in-the-loop methodology, negative results, technical reports and openly licensed code where third-party licenses allow.

### Testable success criteria

1. A fresh install on the documented Linux compute node can reproduce a selected baseline run without privileged manual changes.
2. At least three memory/control conditions can be compared over multiple held-out seeds with published metrics and confidence intervals.
3. The edge inference path is profiled end-to-end, including preprocessing, model runtime, scheduling, actuation latency, and failures.
4. At least one negative or null result is reported with enough data to independently diagnose the failure.
5. Unlicensed/proprietary GTI SDK or model artifacts are **not** redistributed; replacement paths and constraints are documented.

## Fit for AI for Safety & Science Nodes

The project aligns principally with **building and scaling local compute setups** and secondarily with **AI-first bio/neuroscience experiments**. Its contribution would be a small, replicable node for independent experimental work, using a combination of commodity CPUs, specialised edge accelerators, and practical agent-driven test automation.

Rather than treating benchmarks as static demonstrations, the team-of-one design emphasizes safeguards, causally interpretable A/B evaluation, failure reporting, constrained hardware scheduling, and public reproducibility.

## Illustrative funding request (USD 50,000; subject to review)

| Category | Estimated amount | Intended use |
| --- | ---: | --- |
| Reliable compute, RAM, GPU-capable server upgrades | $18,000 | Experiments, training, local model hosting, CI |
| Robot platform, sensors, edge inference modules | $12,000 | Embodied closed-loop tests and spares |
| Storage, backups, networking, power safety | $5,000 | Durable logs, dataset recovery and reliability |
| Experimental operations and benchmark reproduction | $8,000 | Maintenance, repeat trials and travel/shipping where feasible |
| Software integration and technical maintenance | $5,000 | Development infrastructure and stability |
| Documentation, open artifacts and research dissemination | $2,000 | Community review and publication |
| **Total** | **$50,000** | **Planning estimate, not a quote or funding commitment** |

The exact procurement plan depends on availability, export/shipping constraints, licensing, and the grantor's rules. No resources are assumed awarded.

## Limitations and risk management

- **Evidence quality:** local benchmarks and recorded measurements must be independently reproducible; public artifacts are a deliverable, not a current blanket claim.
- **Licensing:** GTI toolchain rights and compatibility require clarification. The work will not distribute vendor-proprietary components without permission.
- **Hardware safety:** avoid unsafe high-load four-channel DMA operation until isolated and characterized; keep tests in simulation before physical robot actuation.
- **Resource limits:** no continuous GPU cluster is presently available; prioritize small controlled studies and staged procurement.
- **Applicant status:** individual researcher resident in Russia; eligibility, payment processing, travel, logistics and any restrictions must be evaluated honestly by the grantor.

## References and evidence entry points

- [ARGOS project repository](https://github.com/winargos42-dotcom/argos)
- [Project overview and verification conventions](https://github.com/winargos42-dotcom/argos/blob/main/docs/PROJECT_OVERVIEW.md)
- [2026–2027 project roadmap](https://github.com/winargos42-dotcom/argos/blob/main/ROADMAP_2026_2027.md)
- [Existing hardware request / in-kind support](https://github.com/winargos42-dotcom/argos/issues/2)

**External academic referee:** Not available at the time of this application. Technical claims and prior work can be examined via the linked repository and supporting experiment artifacts; a referee must not be invented.
