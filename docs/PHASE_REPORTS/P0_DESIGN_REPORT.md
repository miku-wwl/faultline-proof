# Phase 0 — Architecture validation, design freeze and readiness

### Dated compliance correction — 2026-10-19

The A-01 `BLOCKING` label below records the original Phase 0 assessment and is **superseded**. The published lablab.ai general guide generally permits pre-existing open-source libraries and non-AI scaffolding, while directing teams to each event's rules. The reviewed Vultr Agent Rush sources require originality and MIT compliance but show no explicit prohibition of the unchanged, attributed AIG dependency. Current classification: **LOW — Pending Event-Specific Confirmation**, without claiming guaranteed eligibility or organizer approval. Organizer clarification is optional additional assurance, not a prerequisite for bounded infrastructure preparation. This correction is reflected in [ORIGINALITY_AND_REUSE.md](../ORIGINALITY_AND_REUSE.md), [REQUIREMENTS_TRACEABILITY.md](../REQUIREMENTS_TRACEABILITY.md) and [DEPLOYMENT_RUNBOOK.md](../DEPLOYMENT_RUNBOOK.md). Historical findings remain visible below.

Date: 2026-10-19, Pacific/Auckland. Authorized work: research, inspection and documentation only. **Overall: PARTIAL.** Design deliverables and the recorded document checks are complete; event-specific dependency eligibility and all live infrastructure/product gates remain unresolved. This is not future P0 infrastructure acceptance.

## Architecture verdict

**Feasible within the event window with controlled scope**, assuming account/model access and P1 fixture qualification. The reuse question is low risk under the published general guidance, remains subject to event-specific rules, and does not by itself block bounded infrastructure preparation. Plan for 46 focused hours plus 10 contingency within 127 elapsed event hours. No implementation or measured recovery exists yet. The evidence-led SRE replay thesis is preserved; a broad autonomous code fixer, Kubernetes platform or multi-model agent would threaten the deadline.

Keep AIG v0.2.0 at `7261fdd2f47d2b15fabe8faac527eeee37338eb1` unchanged and default five seconds. Its single governed effect is queue admission, not experiment completion. [AIG decision](../AIG_VERSION_DECISION.md) records release/tag/installed API checks and the absence of a Faultline manifest/lock. There is no demonstrated core blocker warranting an upgrade.

Two necessary design closures: exact candidate patch/manifest frozen **before** human approval; atomic enqueue creates a `HELD` job released only on a matching public-gateway `Succeeded` observation. Unknown Actions and ambiguous worker lifecycle remain held/quarantined with no blind retry. No core internals or atomic cross-database guarantee is assumed.

## Ranked architecture audit

| ID / severity | Existing gap and impact | Resolution / remaining gate |
|---|---|---|
| A-01 BLOCKING | **Historical original rating, superseded by the dated correction above:** pre-existing AI runtime and preparation eligibility not explicitly qualified for this event | Current rating LOW — Pending Event-Specific Confirmation; general reuse guidance supports preparation with attribution; event rules remain authoritative; organizer clarification optional |
| A-02 HIGH | Patch generation/revision after approval leaves executable content unreviewed | ADR-009 freezes exact diff and manifest first; revisions need a new trial and fresh consent |
| A-03 HIGH | COMMIT may precede lost ACK/AIG Unknown; eager worker could still execute | HELD/READY release protocol using public `gateway.get`; fault tests required before live trials |
| A-04 HIGH | “Worker lease expiry” lacks safe ownership/lifecycle recovery | Stable epoch, intent-before-Docker-call, no automatic takeover, quarantine and deliberate cleanup |
| A-05 HIGH | Suggested enum not supported by installed AIG schema; confusing Run/trial ID | Six bounded patterned fields; own trial UUID, separate AIG Run; public API schema check recorded separately |
| A-06 HIGH | Baseline fault, equal traffic, p95/error/retry definitions and thresholds underspecified | Fixed 200-request open-loop design, independent upstream count, exact metric/negative-control spec; P1 qualification NOT RUN |
| A-07 HIGH | Public mutation auth and scripted consent are not a product user boundary | Protected single operator, separate recorded decisions; public evidence reads only; browser tests NOT RUN |
| A-08 HIGH | Docker internal network/read-only/non-root labels alone do not establish containment | Actual host/metadata/IPv6/secret/cgroup tests; trusted mock/probe separated; controls NOT RUN |
| A-09 HIGH | Candidate build hooks/arbitrary repair code could run beyond intended scope; copy into read-only root may be denied | Same pinned base image, trusted initializer populates fresh source volumes mounted read-only in service containers; literal-config-only diff; no candidate Docker build |
| A-10 HIGH | Evidence from candidate stdout or attractive green fields could be forged | Trusted probe/mock/evaluator, raw samples and trial/digest binding; missing results remain null/NOT RUN |
| A-11 HIGH | Vultr endpoint/model features, quota and billing not verified for account | Docs confirm protocol direction; model-list route discrepancy, actual IDs/quality/usage/pricing remain P0 gates |
| A-12 HIGH | No application, pyproject, lock, fixture, test harness or product license yet | Truthful preparation state; own-env dependency qualification and license review planned, no facade modules created |
| A-13 MEDIUM | Two active trials and iterative patches increase timing/approval complexity | One active trial and one immutable candidate; no repair loop in v1 |
| A-14 MEDIUM | 30–180 s experiment/demo, token/model delays, five-day effort pressure | Explicit 120 s nominal/180 s hard worker envelope with cleanup reserve; preapproval inference; timed phase/cut plan |
| A-15 MEDIUM | Plain hashes/signatures can be oversold as independent attestation | ZIP internal-integrity verifier plus explicit trusted-host limit; signing/PDF cut |
| A-16 LOW | Master called repository uncreated and suggested removing mandatory AIG if ineligible | Corrected local-state description and stop/report policy conflict; no remote changes |

“Resolved” here means design semantics closed, not implementation security verified. Highest current residuals are A-06, A-08, A-03/A-04 and A-11: reproducible replay, actual containment, ambiguous distributed state and real provider access. A-01 retains its historical BLOCKING value for audit only; it is no longer an active blocker.

## Competition verification

[Requirements/source matrix](../REQUIREMENTS_TRACEABILITY.md) records the official event/live pages, general guidance and unresolved questions. Explicit milestone conversion: Nov 4 04:00 NZDT kickoff, Nov 9 11:00 NZDT cutoff; internal target Nov 8 20:00 NZDT. Detailed overview schedule remains TBA; use live milestone text, not its zero countdown. Video size/duration are general guidance pending actual event form. No registration, residency/prize eligibility, account credit, event-specific reuse confirmation or final form was verified for this participant.

The public competitor descriptions were read, not treated as completed products. Differentiation must rest on SRE incident replay and measured retry/SLO evidence; generic patch-and-proof branding alone overlaps existing team ideas. [Reuse record](../ORIGINALITY_AND_REUSE.md) separates AIG's Oct 13 release from future competition work and plans exact MIT attribution.

## Files created or modified

Created:

- `docs/REQUIREMENTS_TRACEABILITY.md`
- `docs/THREAT_MODEL.md`
- `docs/ORIGINALITY_AND_REUSE.md`
- `docs/INCIDENT_FIXTURE_SPEC.md`
- `docs/AIG_VERSION_DECISION.md`
- `docs/ADRs/ADR-009-TRIAL-EXECUTION-CONTRACT.md`
- `docs/DEPLOYMENT_RUNBOOK.md`
- `docs/DEMO_SCRIPT.md`
- `docs/PHASE_REPORTS/P0_DESIGN_REPORT.md`
- `docs/PHASE_REPORTS/evidence/P0_DESIGN_INSPECTION.md`
- `docs/PHASE_REPORTS/evidence/P0_DOCUMENT_VALIDATION.json`

Modified: `docs/MASTER_DESIGN.md`, narrowly correcting repository state, unsupported schema terminology, exact-patch approval, held admission, revision/concurrency limits, fixture targets, unrun sample statuses and the conflict with mandatory AIG. Product thesis and full design remain intact. Root `AGENTS.md` and `README.md` are preserved. No dependency, application, fixture, infrastructure or test implementation files added.

## Commands, observations and validation

Actual inspections include `git status --porcelain=v1`, `git ls-files`, `git log -1`, `git remote -v`; complete root/master/README and request reads; read-only `git ls-remote` release resolution; upstream reference downloads; installed `importlib.metadata`, public `inspect.signature`/source, RECORD hash verification; `uv pip check` on the pre-existing external consumer environment; official source retrieval and embedded rule-book text extraction. No other repository was changed.

The installed-package inspection is **not** a Faultline install: own manifest/lock/environment are absent. Public schema/Plan parsing and static documentation checks are design validation, not enqueue, race, worker, sandbox or end-to-end product tests. See [inspection record](evidence/P0_DESIGN_INSPECTION.md) and [machine validation](evidence/P0_DOCUMENT_VALIDATION.json) for actual results, hashes and limitations. Do not inherit upstream's published test totals as this repository's tests.

**NOT RUN:** product pytest/TypeScript tests; AIG consumer workflow or ledger mutation; enqueue/concurrency/crash/recovery; Docker/container creation or security probes; incident baseline/candidate/replay/evaluator; model inference; Vultr API/account inspection or provisioning; deployment/TLS/public browser E2E; evidence-export verifier implementation; demo recording; commit/push/tag/release/submission. Cloud cost incurred by this task: no billable requests/resources initiated.

## Security decisions and readiness

Design ready: one governed effect; public API composition/signatures; flat bounded schema; stable binding/scope; exact reviewed manifest; queue transaction/receipt; held-job release; no redispatch after uncertainty; private human controls/public reader; fixed replay/evaluator; trusted measurements; testable containment, lifecycle and artifact provenance.

Infrastructure preparation is not blocked solely by the pending AIG reuse confirmation. Infrastructure creation and paid inference still require operation-specific authorization, allowed timing, account access, a reviewed region/SKU/live price, domain/operator setup and actual Linux/cgroup/model qualification. If event rules change or explicitly prohibit this dependency, reassess before competition submission. These limits prohibit a claim of runtime readiness. Stop here; no automatic phase advancement.

## Next phase and copy-ready execution prompt

Exact next phase: **P0 — Vultr infrastructure and actual inference connectivity**, after the above gates. Recommended **Codex Sol, Extra High** for initial identity/security/deployment qualification; use High for routine bounded implementation once those contracts are settled. The following prompt has **not** been executed:

```text
Use Codex Sol with Extra High effort in VS Code. Execute only Faultline Proof P0 infrastructure readiness, not P1 incident implementation.

Read root AGENTS.md, docs/MASTER_DESIGN.md, docs/AIG_VERSION_DECISION.md, docs/REQUIREMENTS_TRACEABILITY.md, docs/DEPLOYMENT_RUNBOOK.md, docs/THREAT_MODEL.md, docs/ADRs/ADR-009-TRIAL-EXECUTION-CONTRACT.md and docs/PHASE_REPORTS/P0_DESIGN_REPORT.md; inspect Git state first.

Reverify current official event/live rules and the permitted implementation window. The published general guidance generally allows pre-existing open-source libraries and non-AI scaffolding, subject to event rules; current AIG reuse risk is LOW — Pending Event-Specific Confirmation. Organizer clarification is optional and is not a prerequisite for bounded infrastructure preparation. If official rules explicitly conflict, report the conflict and follow root AGENTS. Do not hide, bypass or remove AIG.

Prepare the smallest concrete Vultr VM/region/SKU/HTTPS/model connectivity plan with live prices, resource expiry, private credential handling and total cost estimate. This prompt authorizes local preparation and read-only research; it does not authorize billable calls, provisioning or deployment. Obtain an explicit resource/call-specific user approval of the final proposal and cost ceiling before those operations. Do not ask for approval of an unspecified plan.

Once those gates and explicit approvals exist, create Faultline's own Python 3.13 pyproject/lock and verify installed agentic-intent-gate==0.2.0 at 7261fdd2f47d2b15fabe8faac527eeee37338eb1, imported from its site-packages, using the default 5-second profile and no core edits. Provision only the approved VM, protect API/runner/credentials, verify HTTPS from an actual external browser, perform only the approved minimum real Vultr Serverless Inference connectivity call, and qualify a harmless resource-bounded sandbox with observed cleanup. Record requested/actual model identity and real provider/timing/usage evidence; no fallback or fake metrics.

Do not implement the incident fixture, repair Agent, trial worker/queue product or full frontend in P0. Do not run unrelated Docker/Kubernetes operations, automatic inference retries, real production effects, commit/push/tag/release or submit. Report PASS/PARTIAL/BLOCKED with exact files, commands, evidence, unresolved risks, actual costs/resource inventory and shutdown status. Stop at P0; recommend the next phase without executing it.
```
