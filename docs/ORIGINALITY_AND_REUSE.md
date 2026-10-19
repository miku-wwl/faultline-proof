# Originality, reuse and pre-kickoff boundary

Date: 2026-10-19. Status: **Preparation record; event-specific reuse eligibility UNVERIFIED**.

Faultline builds the incident product and reuses unchanged AIG for consent-bound queue admission. AIG is not presented as new competition work. Competition functionality must begin only in the allowed window, with the root AGENTS phase boundary and separate authorization respected.

## Provenance inventory

| Component | Original source/date | Classification | License / required attribution | Evidence |
|---|---|---|---|---|
| AIG runtime | Weilai Wang; annotated release Oct 13, 2026 | Pre-existing external dependency, unchanged | MIT; retain copyright and license in distributions/notices | [Pinned license](https://github.com/miku-wwl/agentic-intent-gate/blob/7261fdd2f47d2b15fabe8faac527eeee37338eb1/LICENSE), [version decision](AIG_VERSION_DECISION.md) |
| Initial Faultline design/root instructions | Local HEAD `79059c132cd2242ad826f8613b284f98e2f3dbc4`, inspected Oct 19 | Existing preparation; three tracked Markdown files, no application | Repository product license not yet present | `git ls-files`, inspection evidence |
| Phase 0 review/specifications | This documentation change, Oct 19 | Pre-kickoff research/design; not an executed product | Preserve authorship/provenance in eventual repo history | [Report](PHASE_REPORTS/P0_DESIGN_REPORT.md) |
| FastAPI/httpx/jsonschema/uvicorn and dependencies | Upstream package sources, exact versions TBD | Future third-party dependencies | Resolve licenses/notices from actual lock/SBOM at P0/P5 | No Faultline lock/install yet |
| Docker/Linux/base image/frontend packages | Exact distributions/digests TBD | Future platform/dependencies | Audit image/package licenses and retain required notices | P0/P1 provenance gate |
| Incident fixture/mock/replay/evaluator | To be authored during allowed window | Planned original competition work | Intended project MIT policy, repository owner to confirm grant | NOT IMPLEMENTED |
| Vultr proposal integration, queue/worker, UI and Passport | To be authored during allowed window | Planned original product integration | Intended project policy plus third-party notices | NOT IMPLEMENTED |
| Generated candidate patch | Future actual Vultr response | Model-assisted competition artifact; disclose origin | Record provider/model/call/digest and review provenance; no claim of guaranteed novelty | NOT GENERATED |

Do not copy AIG internal modules, source execution mechanisms or its developer-only root policy. Dependency integration uses the installed public API. Existing reference sample is an integration reference; any adapted consumer code must be attributed, and scripted sample consent must never be described as a human decision.

## Eligibility interpretation

The [official event](https://lablab.ai/ai-hackathons/vultr-hackathon) requires originality and MIT compliance. The [general guide](https://lablab.ai/guide/ai-hackathons) discusses reuse subject to each event. This is **not** an event-specific approval of this pre-existing AI runtime. [Rule book](https://lablab.ai/hackathon-rules) also does not supply a located AIG-specific or prebuild exception. Questions and status are tracked as O-07 in [requirements](REQUIREMENTS_TRACEABILITY.md).

No organizer contact, enrollment, terms acceptance or license publication occurred in Phase 0. Preserve a written organizer answer before making an eligibility claim. If reuse is disallowed, stop and report the conflict to the user: root AGENTS mandates unchanged pinned AIG. Do not remove it, replace governance or hide reuse without an explicit separately reviewed change to that mandate.

## Differentiation without unsupported competitor claims

Public team descriptions for [PatchProof](https://lablab.ai/ai-hackathons/vultr-hackathon/patchproof) and [Airlock](https://lablab.ai/ai-hackathons/vultr-hackathon/airlock) were re-read. PatchProof describes vulnerability repair and adversarial verification; Airlock describes a sandbox control plane. These are team ideas, not verified delivered products. Their presence means “patch + sandbox + proof” alone is weak differentiation.

Faultline's own defensible presentation is a bounded SRE incident: fixed replay, error and retry numerators/denominators, independent upstream instrumentation, exact human-reviewed config candidate, recovery/containment/teardown separated, and a reproducible artifact bundle. This is a positioning judgment, not an exclusive novelty claim or assurance of an award. Do not borrow competitor code, phrases, branding or screenshots.

## Planned release notice

Eventual README and `THIRD_PARTY_NOTICES` should state:

> Faultline Proof uses Agentic Intent Gate v0.2.0, commit 7261fdd2f47d2b15fabe8faac527eeee37338eb1, by Weilai Wang, under MIT. It is an unchanged pre-existing runtime for Plan validation, approval binding, independent authorization and bounded Action execution. Faultline's incident fixtures, Vultr integration, durable trial queue/worker, evaluator, dashboard and Evidence Passport are separate product work; their actual development dates and state are recorded in this repository.

Include the upstream full MIT notice in applicable distributed copies and audit the actual dependency/image inventory. No consumer LICENSE is added merely on an assumption about authority. Root policy establishes the intended MIT-compatible direction; final publication remains a later explicit action.
