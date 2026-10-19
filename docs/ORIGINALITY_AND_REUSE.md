# Originality, reuse and pre-kickoff boundary

Date: 2026-10-19. Status: **LOW — Pending Event-Specific Confirmation**. This is a risk rating, not an event approval or guaranteed eligibility.

Faultline builds the incident product and reuses unchanged AIG for consent-bound queue admission. AIG is not presented as new competition work. Competition functionality must begin only in the allowed window, with the root AGENTS phase boundary and separate authorization respected.

## Provenance inventory

| Component | Original source/date | Classification | License / required attribution | Evidence |
|---|---|---|---|---|
| AIG runtime | Weilai Wang; annotated release Oct 13, 2026 | Pre-existing external dependency, unchanged | MIT; retain copyright and license in distributions/notices | [Pinned license](https://github.com/miku-wwl/agentic-intent-gate/blob/7261fdd2f47d2b15fabe8faac527eeee37338eb1/LICENSE), [version decision](AIG_VERSION_DECISION.md) |
| Initial Faultline design/root instructions | Local HEAD `79059c132cd2242ad826f8613b284f98e2f3dbc4`, inspected Oct 19 | Existing preparation; three tracked Markdown files, no application | Repository product license not yet present | `git ls-files`, inspection evidence |
| Phase 0 review/specifications | This documentation change, Oct 19 | Pre-kickoff research/design; not an executed product | Preserve authorship/provenance in eventual repo history | [Report](PHASE_REPORTS/P0_DESIGN_REPORT.md) |
| Python environment and generic preflight checks | Authorized local readiness sprint, Oct 19, 2026 | Pre-kickoff reusable environment preparation; no incident/agent/worker/frontend | Preserve provenance separately from competition product | [Readiness report](PHASE_REPORTS/PRE_HACKATHON_READINESS_REPORT.md) |
| FastAPI/httpx/jsonschema/uvicorn and dependencies | Upstream distributions, exact versions in `uv.lock` | Installed third-party dependencies, not original competition work | Review installed licenses/notices before distributing; pin does not waive notices | [Installed dependency evidence](PHASE_REPORTS/evidence/PRE_HACKATHON_AIG.json); lock is environment preparation |
| Docker/Linux/base image/frontend packages | Exact distributions/digests TBD | Future platform/dependencies | Audit image/package licenses and retain required notices | P0/P1 provenance gate |
| Incident fixture/mock/replay/evaluator | To be authored during allowed window | Planned original competition work | Intended project MIT policy, repository owner to confirm grant | NOT IMPLEMENTED |
| Vultr proposal integration, queue/worker, UI and Passport | To be authored during allowed window | Planned original product integration | Intended project policy plus third-party notices | NOT IMPLEMENTED |
| Generated candidate patch | Future actual Vultr response | Model-assisted competition artifact; disclose origin | Record provider/model/call/digest and review provenance; no claim of guaranteed novelty | NOT GENERATED |

Do not copy AIG internal modules, source execution mechanisms or its developer-only root policy. Dependency integration uses the installed public API. Existing reference sample is an integration reference; any adapted consumer code must be attributed, and scripted sample consent must never be described as a human decision.

## Eligibility interpretation

The [published lablab.ai general guidance](https://lablab.ai/guide/ai-hackathons) says pre-existing open-source libraries and prior non-AI scaffolding are generally allowed, while the core AI-powered functionality is generally built during the event window; it explicitly directs participants to check each event's own rules. AIG fits the general category of an existing MIT-licensed infrastructure dependency: it supplies bounded Plan validation, approvals and execution governance, while Faultline's incident diagnosis, remediation candidate, replay, sandbox worker, evaluation and Evidence Passport are the competition-specific product to build during the permitted window.

The [Vultr Agent Rush page](https://lablab.ai/ai-hackathons/vultr-hackathon) requires original, MIT-compliant submissions, but the reviewed published sources do not identify an explicit rule prohibiting this pinned AIG reuse, nor do they provide explicit organizer approval. Therefore the active risk is **LOW — Pending Event-Specific Confirmation**, not a finding of guaranteed eligibility or a documented violation. Official event rules remain authoritative if they add a narrower requirement. A direct organizer clarification is optional additional assurance, not a prerequisite for bounded infrastructure preparation. Read-only rule checks and the root AGENTS pre-kickoff boundary still apply; competition-specific core functionality must be developed in the permitted window. See O-07 in [requirements](REQUIREMENTS_TRACEABILITY.md).

AIG remains pinned and unchanged at v0.2.0 / `7261fdd2f47d2b15fabe8faac527eeee37338eb1`. Preserve attribution and the applicable MIT copyright/license notices. No organizer contact, enrollment, terms acceptance or license publication occurred in Phase 0. If a future official event rule expressly disallows AIG, document the conflict and follow the governing repository instructions rather than claiming eligibility or silently concealing/removing the dependency.

## Differentiation without unsupported competitor claims

Public team descriptions for [PatchProof](https://lablab.ai/ai-hackathons/vultr-hackathon/patchproof) and [Airlock](https://lablab.ai/ai-hackathons/vultr-hackathon/airlock) were re-read. PatchProof describes vulnerability repair and adversarial verification; Airlock describes a sandbox control plane. These are team ideas, not verified delivered products. Their presence means “patch + sandbox + proof” alone is weak differentiation.

Faultline's own defensible presentation is a bounded SRE incident: fixed replay, error and retry numerators/denominators, independent upstream instrumentation, exact human-reviewed config candidate, recovery/containment/teardown separated, and a reproducible artifact bundle. This is a positioning judgment, not an exclusive novelty claim or assurance of an award. Do not borrow competitor code, phrases, branding or screenshots.

## Planned release notice

Eventual README and `THIRD_PARTY_NOTICES` should state:

> Faultline Proof uses Agentic Intent Gate v0.2.0, commit 7261fdd2f47d2b15fabe8faac527eeee37338eb1, by Weilai Wang, under MIT. It is an unchanged pre-existing runtime for Plan validation, approval binding, independent authorization and bounded Action execution. Faultline's incident fixtures, Vultr integration, durable trial queue/worker, evaluator, dashboard and Evidence Passport are separate product work; their actual development dates and state are recorded in this repository.

Include the upstream full MIT notice in applicable distributed copies and audit the actual dependency/image inventory. No consumer LICENSE is added merely on an assumption about authority. Root policy establishes the intended MIT-compatible direction; final publication remains a later explicit action.
