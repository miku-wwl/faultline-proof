# Requirements traceability and Phase 0 freeze

Verified on 2026-10-19, Pacific/Auckland. **Design preparation only.** `CONFIRMED` below describes a retrieved source, not product compliance. Every product runtime acceptance test is **NOT RUN**.

Later on the same date, the authorized [pre-hackathon readiness sprint](PHASE_REPORTS/PRE_HACKATHON_READINESS_REPORT.md) qualified a project-local pinned Python/AIG environment and generic local Docker controls. It rechecked public schedule/rules/catalogs; these local checks do not satisfy the cloud/product acceptance gates below. The current dependency state is in [AIG version decision](AIG_VERSION_DECISION.md).

## Official sources and open eligibility gates

| ID | Requirement / finding | Source and authority | Status |
|---|---|---|---|
| O-01 | Kickoff Nov 3 15:00 UTC; submission Nov 8 22:00 UTC | [Live dashboard](https://lablab.ai/ai-hackathons/vultr-hackathon/live), explicit milestone text | CONFIRMED; ignore its zeroed countdown |
| O-02 | Vultr VM backend; agent LLM calls through Serverless Inference | [Event requirements](https://lablab.ai/ai-hackathons/vultr-hackathon) | CONFIRMED |
| O-03 | Vultr sandbox execution, verifiable results, multistep product workflow, process/secret/resource/lifecycle controls | Same event source | CONFIRMED |
| O-04 | Public app/repository, documentation, video with containment, slides and cover listed | Same event source, submission sections | CONFIRMED |
| O-05 | Original, MIT-compliant submission; teams 1–6 | Same event source | CONFIRMED; personal eligibility/enrollment NOT VERIFIED |
| O-06 | Video within 5 minutes and under 300 MB | [General submission guidance](https://lablab.ai/ai-articles/hackathon-guidelines) | General guidance; event form limits NOT VERIFIED |
| O-07 | Pre-existing AIG/scaffolding eligibility and permissible pre-kickoff preparation | [General guide](https://lablab.ai/guide/ai-hackathons), [event page](https://lablab.ai/ai-hackathons/vultr-hackathon), [rule book](https://lablab.ai/hackathon-rules) | **Reuse risk LOW — pending event-specific confirmation**; no explicit prohibition or approval identified |

O-01 converts to **2026-11-04 04:00 NZDT** kickoff and **2026-11-09 11:00 NZDT** cutoff. Local internal submission target is **2026-11-08 20:00 NZDT**. The build interval is 127 hours, not six full engineering days. Event overview's detailed schedule remains TBA; the live milestone text supplies the explicit UTC clocks. Recheck before implementation and submission.

The published general guide says use of open-source libraries, starter templates, and prior non-AI scaffolding is generally allowed; it expects core AI functionality to be built during the event and directs teams to event-specific rules. The Vultr event requires original MIT-compliant work. The reviewed sources do not explicitly prohibit the unchanged AIG pin or expressly approve it. Classify this unresolved question as **LOW — Pending Event-Specific Confirmation**, not as a documented violation or guaranteed eligibility. Organizer clarification is optional additional assurance and is not a prerequisite for bounded infrastructure preparation. The Phase 0 implementation boundary still applies: build Faultline's competition-specific core during the permitted window. Recheck official rules as they change. The rule book was retrieved through its embedded MDX source because the text-only browser returned an empty shell. General rule book says cover optional; event lists a cover: prepare one. Do not rely on general grace periods or informal deadline extensions.

Optional questions for the organizer (draft only; **no messages sent**): Is unchanged MIT AIG released on Oct 13 permissible with full attribution, and are any event-specific reuse restrictions planned? Other questions remain about exact pre-kickoff work, submission limits and participant eligibility. These are useful additional assurance and readiness checks, not a prerequisite for bounded infrastructure preparation. Keep the root policy's prohibition on competition-specific implementation before the permitted window, disclose reuse, and check official rule updates. Do not claim individual eligibility or event-specific approval without evidence.

## Product acceptance map

| ID | Frozen requirement | Design owner | Planned acceptance / artifact | Gate |
|---|---|---|---|---|
| C-01 | Vultr-only model provenance, no fallback | [Deployment](DEPLOYMENT_RUNBOOK.md) | Real redacted request/response/model/timing/usage; mismatched model denied | P0/P2 |
| C-02 | Backend/runner/sandboxes actually on Vultr | Deployment | VM + service + HTTPS + container lifecycle correlation | P0 |
| C-03 | Real isolated code/config execution | [Fixture](INCIDENT_FIXTURE_SPEC.md) | Actual image/container IDs, output and teardown | P1/P2 |
| G-01 | Exact Plan Approval separate from Authorization | [ADR-009](ADRs/ADR-009-TRIAL-EXECUTION-CONTRACT.md) | Authenticated human events, stored Run/Plan/Action versions and grant references | P2 |
| G-02 | Wrong identity, stale/missing consent denied | ADR-009; [AIG decision](AIG_VERSION_DECISION.md) | Parameterized denial tests; no queue rows/effects | P2 |
| G-03 | Unique durable queue effect under default budget | ADR-009 | Duplicate/concurrent/conflict/COMMIT tests, reopened rows and receipt | P2 |
| G-04 | Unknown never auto-redispatches | ADR-009 | Lost ACK / finish / restart tests, HELD/quarantine, no sandbox start | P2/P3 |
| G-05 | Exact patch frozen before approval; no revision in same trial | ADR-009 | Changed patch/manifest invalidates consent; immutable digest assertions | P2 |
| G-06 | AIG success means admission only | ADR-009 | UI/API show separate admission/worker/recovery/containment/cleanup states | P2/P4 |
| R-01 | Baseline actually degrades | Fixture | 200 raw quote samples, upstream attempts; failure predicates true | P1 |
| R-02 | Genuine Vultr candidate, narrow config surface | Fixture | Real model evidence, validated diff/AST/tree, no stored repair substitution | P2 |
| R-03 | Equal-condition candidate replay | Fixture | Matching immutable condition digests, fresh mocks, same 200 inputs | P2 |
| R-04 | Deterministic honest verdict | Fixture | Negative controls; incomplete/equivalence/cleanup cases cannot PASS | P2/P3 |
| S-01 | Host marker inaccessible | [Threat model](THREAT_MODEL.md) CT-01 | Actual denial + independent unchanged host hash | P3 |
| S-02 | Time/resource bounds enforced | Threat model CT-02/07 | Cgroup counters, timed termination, API health, exact cleanup | P0/P3 |
| S-03 | No secrets/socket; constrained egress | Threat model CT-05/06 | Redacted config/mount audit and actual canary connectivity tests | P0/P3 |
| S-04 | Hostile log cannot grant authority | Threat model CT-03/04 | Unsafe output visible, forbidden patch denied, no privileged effect | P3 |
| S-05 | Worker ambiguity quarantines | Threat model CT-08/10 | Crash/lifecycle matrix and resource inventory without second run | P3 |
| E-01 | Trial-bound, tamper-detectable Evidence Passport | Deployment; ADR-009; Fixture | Offline recomputation of artifact/manifest/diff/variant relationships | P4 |
| D-01 | Public inspectability, protected mutations | Deployment | Fresh public browser reads; anonymous/CSRF/ownership mutation denials | P0/P4 |
| D-02 | Complete honest submission | [Demo](DEMO_SCRIPT.md); [reuse](ORIGINALITY_AND_REUSE.md) | Fresh smoke bundle, usable links, video/deck/cover/license/README | P5 |
| Q-01 | Bounded cost/latency; all attempts retained | Deployment | Server quota records and observed timings; live pricing before spend | P0–P5 |
| Q-02 | Repeated qualification, no cherry-picking | Fixture | Three predeclared qualification pairs, including failed observations | P1/P4 |

## Frozen MVP and cuts

Keep one `retry-storm-503` workflow, one literal-config candidate, one governed enqueue, one active trial, protected single operator, public evidence reader, JSON/ZIP Passport and the mandatory `suspicious-log-injection` negative input plus actual runtime containment probe. Choose React/TypeScript/Vite static UI, Python 3.13/FastAPI, two separate SQLite stores, one independently managed worker/runner and one Vultr VM. No Kubernetes, general orchestration framework, arbitrary repositories, browser agent, MCP tools, production deployment, payment integration or automatic candidate revision.

Cut order: optional memory incident -> animations -> PDF/signatures -> SSE (bounded polling remains) -> multiple models -> multi-user accounts -> extra repair revisions (already excluded from v1). Never cut exact consent, durable admission, real baseline/candidate execution, deterministic measurement, containment, teardown or traceability. Scope extensions require a new reviewed phase decision, not a silent implementation shortcut.

Runtime evidence status for every row above: **NOT RUN**. Phase 0 inspection evidence is separately recorded in [P0 design report](PHASE_REPORTS/P0_DESIGN_REPORT.md); it cannot satisfy a cloud/product gate.
