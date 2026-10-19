# FAULTLINE PROOF
## Competition-grade Master Design & Execution Specification

> **Tagline:** Fix the incident. Prove the recovery. Contain the risk.  
> **Repository:** `miku-wwl/faultline-proof` (existing local consumer repository; implementation not present at Phase 0 inspection)<br>
> **Competition:** Vultr: Agent Rush Hackathon 2026 — *Blast Radius Zero: Safe Agent Execution on Vultr*  
> **Authoring baseline:** 2026-10-19, NZDT  
> **Spec status:** `DESIGN / PRE-KICKOFF` — not implementation evidence  
> **Goal:** A compelling, working, publicly reachable, verifiably sandboxed **SRE incident remediation agent**, not a generic coding agent or sandbox framework.

**2026-10-19 Phase 0 clarification:** [ADR-009](ADRs/ADR-009-TRIAL-EXECUTION-CONTRACT.md) freezes the exact candidate before approval and holds committed jobs until AIG success is confirmed. The [fixture specification](INCIDENT_FIXTURE_SPEC.md), [threat model](THREAT_MODEL.md), [requirements](REQUIREMENTS_TRACEABILITY.md) and [deployment runbook](DEPLOYMENT_RUNBOOK.md) resolve v1 implementation details. These are design contracts, not execution evidence; see the [Phase 0 report](PHASE_REPORTS/P0_DESIGN_REPORT.md).

---

## 0. Non-negotiable product thesis

**Faultline Proof is an AI incident-response system that safely fixes a realistic service outage in an isolated Vultr-hosted incident twin, measures the counterfactual *before vs. after*, and publishes an auditable evidence passport. It never autonomously changes the original production-like reference service.**

Pitch: *"When AI says an outage is fixed, teams need proof. Faultline uses an isolated incident twin to execute the candidate repair, replay the same failure conditions, verify recovery and safety invariants, and deliver a reviewable patch with evidence—without touching production."*

### What judges see in 60 seconds

1. The **Incident Console** opens with a failing service: elevated 5xx/error rate, live log samples, and a clear incident card.
2. Vultr inference generates a diagnosis and a **real code/config patch**; the user reviews the bounded plan.
3. The **AIG approval and separate action authorization** precede one durable sandbox-job admission.
4. Two actual isolated executions replay equivalent requests: **baseline (broken)** and **candidate (patched)**.
5. A green/red **Outcome Comparator** shows test results, error-rate improvement and absence of regressions.
6. A **Containment Moment** shows one deliberately unsafe operation contained or terminated, with the host reference unaffected.
7. An exportable **Evidence Passport** includes provenance, hashes, test logs, container lifecycle observations and an actionable patch. The user may export—**no automatic deployment to production**.

### Explicit non-goals

- No generic PaaS or agent framework; no new Kubernetes operator or cloud provisioner.
- No autonomous production deployment, external GitHub PR mutation, shell access to arbitrary repositories, or arbitrary public URL imports in the MVP.
- No false claim that a single demo proves mathematical isolation, zero blast radius for every threat, exact-once effects, production SLO compliance, or complete digital-twin fidelity.
- No multi-agent role theater; orchestrate one real model-assisted workflow with deterministic validators.
- No second execution pattern (browser automation) until core Pattern A, containment, and submission materials are complete.

---

## 1. Official constraints & source-of-truth checklist

**Official competition:** https://lablab.ai/ai-hackathons/vultr-hackathon  
**Live schedule:** https://lablab.ai/ai-hackathons/vultr-hackathon/live  
**Presentation guidance:** https://lablab.ai/ai-articles/hackathon-guidelines

- Kickoff / registration closes: **2026-11-03 15:00 UTC = 2026-11-04 04:00 NZDT**.
- Submission closes: **2026-11-08 22:00 UTC = 2026-11-09 11:00 NZDT**. **Internal deadline: 2026-11-08 evening NZDT**, leaving submission buffer.
- Backend must run on a **Vultr VM**; Vultr is the central agent-control infrastructure.
- **All agent LLM calls must use Vultr Serverless Inference** (base URL officially stated: `https://api.vultrinference.com/v1`). Local/mock models only for offline development tests; never a substituted production demo.
- Sandboxed code execution or sandboxed browser use; real executed output; multi-step workflow; process/secret/resource/lifecycle controls.
- Public web demo, public GitHub repository, setup/docs, presentation video, slides and cover image.
- At least one real **containment moment** in the video.
- Publication calls for **original, MIT-compliant** work. Verify official rule book and permitted use of pre-existing components before kickoff. Keep explicit attribution.
- Follow the latest official page if times/extra tracks change.

**Competition similarity warning (as observed 2026-10-19):** public teams named **PatchProof** (adversarial auto-fix with patches) and **Airlock** (sandbox control-plane). Our distinct proposition is **operational outage remediation, measurable baseline/candidate incident replay, policy-bound approval, an auditable non-deployment recovery decision**, not generic patching or platform controls.

---

## 2. Product users, problem, defensible wedge

**Primary user:** on-call SRE / Platform Engineer at a SaaS company.

**The costly decision:** during an incident, a plausible AI fix may create a regression, worsen error budget burn or expand operational blast radius. Existing chat outputs, code reviews and isolated test logs do not by themselves show a faithful before/after experiment with service-level probes.

**Product promise:** a single *"Should we promote this candidate fix for human review?"* screen backed by executable evidence.

**Three unique product primitives:**

1. **Incident Twin:** a disposable, explicitly bounded copy of a *known fixture* that reproduces the initial failure on Vultr (do not claim to mirror a real enterprise production system).
2. **Counterfactual Recovery Trial:** execute *the same fixture version, request scenario, load profile and random seed* against baseline and candidate; calculate objective deltas and prevent unverifiable cherry-picking.
3. **Evidence Passport:** collect candidate patch SHA, image/fixture digests, exact planned tests, observed outcomes, containment checks, timestamps, cleanup status and governance event IDs. Show what is observed versus inferred. Label incomplete/unknown honestly.

**MVP acceptance story:** an evaluator can run a preseeded incident in a real public application, review the plan, approve and separately authorize execution, watch evidence stream, inspect the resulting patch, and independently review actual measured baseline/candidate reports.

---

## 3. Product UX and information design

**Design:** sophisticated incident-operations console, dark/neutral theme, strong typography, readable in a 5-minute recorded walkthrough. Do not sacrifice functionality for decoration.

### Main views

1. **Incident Queue / Dashboard** — 2 preseeded incidents, run status, severity, symptom, safe-run buttons; no open-ended arbitrary code input in public MVP.
2. **Incident Detail** — error-rate trend, relevant logs/trace samples, service topology thumbnail, affected endpoint and known reproduction protocol. A top-line status explicitly distinguishes **REFERENCE: NOT MODIFIED**.
3. **Plan Review** — diagnosis, assumptions, files to change, predicted effect, immutable plan digest, policy and scope, user approval then separate action authorization.
4. **Live Experiment** — state machine, bounded execution stages, baseline/candidate progress, received live logs, model call count, timeout budget, sandbox IDs and cleanup status.
5. **Proof Comparison** — left/right cards for baseline and candidate, absolute counts and denominators, regression invariants, risk checks, actual patch diff, and final `PROVEN_FOR_THIS_SCENARIO | REJECTED | INCONCLUSIVE`.
6. **Evidence Passport** — verifiable JSON and downloadable Markdown summary, source artifact hashes, signed or authenticated manifest only if correctly implemented, explicit trust and limitations section.

### Vital UX rule

**Never display PASS based on a model statement.** The status derives from hard verifier predicates and recorded trusted probe observations. Clearly differentiate *"analysis suggests"*, *"experiment observed"*, and *"production deployment not performed"*.

### Judges' guided demo

An introductory banner with a predefined **Run Guided Incident Demo** link may open a fixture and walk through normal *human-initiated* Review → Approval → Authorization. It must not silently fabricate consent, bypass enforcement or enqueue a job on page load.

---

## 4. Domain model and reference incidents

### Incident A (mandatory, demo golden path): `retry-storm-503`

- **Fixture:** a small production-like Python FastAPI service with a controlled mock upstream; intentionally bad timeout/retry/backoff configuration induces recurring 503 responses under a deterministic request replay.
- **Symptom:** elevated `/checkout/quote` 5xx, correlated upstream timeout/retry logs; `/health` remains responsive.
- **Candidate repair:** v1 freezes one narrow unified patch to existing integer literals in `service/config.py` before approval (see fixture spec). Changes to retry implementation, tests, runner or safety harness are excluded.
- **Baseline:** reproduce failure using scenario seed and fixed request stream.
- **Candidate:** run the approved patched source on the same pinned base image in a separate disposable sandbox and replay **exactly equivalent** scenario; compare error rate, p95 latency, functional tests, health endpoints, and invariant checks.
- **Success:** verifiable improvement meeting calibrated thresholds, zero disallowed changed files, no regression, clean lifecycle. Model must not be able to edit the verifier or fixture scenario definition.

### Incident B (mandatory, negative-policy path): `suspicious-log-injection`

- Same seeded service or a second manifest includes an **untrusted log line** that asks the model to ignore instructions, read host credentials, or access a path outside the workspace. Treat this text as hostile data.
- The model may only propose a bounded patch, never command execution authority. Wrong-path proposal is rejected by the patch validator; attempts to read a host-only sentinel from within the sandbox must fail without affecting the host.
- This is a real policy/containment test. If the model obeys the malicious log, mark the model behavior unsafe and show **rejection**, not a magically successful remediation.

### Optional Incident C (stretch): `memory-leak-worker`

- Bounded memory/pid leak fixture; observe cgroup memory termination, safe teardown, and no host impact. Drop this if golden path or video is incomplete.

### Fixture contracts

Each fixture has an immutable `manifest.json` with:

- `fixture_id`, `fixture_revision`, `source_tree_sha256`, `image_digest` after build;
- immutable `scenario_id`, `scenario_seed`, test harness digest, allowed patch paths;
- bounded CPU/memory/pid/time budgets;
- baseline degradation criteria, candidate recovery thresholds, regression invariants;
- what cannot be proved by this fixture.

Freeze fixture/test/harness **before** an evaluated candidate is generated. Persist immutable versions for every run. Do not allow model outputs to edit fixtures, scenario seeds, probe thresholds, harness commands or expected results.

---

## 5. System architecture

```mermaid
flowchart TB
    Browser[Public Next.js / React Console] --> API[FastAPI on Vultr VM]
    API --> Model[Vultr Serverless Inference]
    API --> AIG[AIG v0.2.0 Governance Runtime]
    AIG --> Dispatch[One trusted enqueue_incident_trial/1 executor]
    Dispatch --> DB[(Consumer SQLite: Jobs + Evidence)]
    DB --> Worker[Trusted Vultr Sandbox Runner]
    Worker --> Docker[Docker Engine - trusted runner only]
    Docker --> Base[Disposable Baseline Container]
    Docker --> Candidate[Disposable Candidate Container]
    Docker --> Probe[Isolated Probe Runner]
    Worker --> Evidence[(Trusted Evidence & Receipts)]
    Evidence --> API
    API --> Browser
```

### Deployment boundaries

- **Vultr VM:** nginx/Caddy TLS terminator; `web` (static frontend or Next.js), `api` (FastAPI + AIG integration), trusted `worker`, SQLite persistent volume and evidence store. The **trusted runner alone** may reach Docker daemon API, never the API web process or the sandbox containers.
- **Vultr Serverless Inference:** all task-related planning/diagnosis/patch/explanation model requests, with recorded provider/model/latency/token usage. Never pass Vultr inference secrets into sandbox environment or logging.
- **Untrusted sandbox:** one isolated container per baseline/candidate run, and a separate trusted verifier/probe container or constrained process; no host mounts, no Docker socket, no cloud API key, no direct internet egress, no production credentials.
- **Trusted storage:** SQLite WAL with explicit migrations and separate *AIG gate ledger* versus *consumer jobs/effects ledger*. Immutable evidence files stored behind an allowlisted artifact-reading API. Never serve arbitrary filesystem paths.
- **Public exposure:** only HTTPS and explicit public API paths. Management, runner and Docker APIs are inaccessible from the public network.

### Why no K8s for MVP?

A single correctly configured Vultr VM plus hardened ephemeral containers fulfills Pattern A with fewer failure points in five effective development days. Existing KPCP assets can inform design, but K8s control-plane integration is a **stretch goal only** and would create technical and originality risk.

---

## 6. Existing Agentic Intent Gate integration — exact scope boundary

**Mandatory root policy:** copy upstream [`docs/AGENTS-dependence.md`](https://github.com/miku-wwl/agentic-intent-gate/blob/main/docs/AGENTS-dependence.md) to **root `AGENTS.md`**. Follow the guidance without replacing or silently weakening it. Read also:

- https://github.com/miku-wwl/agentic-intent-gate/blob/main/docs/V0.2.0-CONSUMER-HANDOFF.md
- https://github.com/miku-wwl/agentic-intent-gate/blob/v0.2.0/docs/ADAPTER_GUIDE.md
- https://github.com/miku-wwl/agentic-intent-gate/blob/v0.2.0/examples/consumer/app.py

Dependency (merge into existing project dependencies; do not overwrite them):

```toml
"agentic-intent-gate @ git+https://github.com/miku-wwl/agentic-intent-gate.git@7261fdd2f47d2b15fabe8faac527eeee37338eb1"
```

**Version:** v0.2.0, Python 3.13, MIT, **Git commit pin**, not assumed PyPI package. Verify installed external dependency, public API, exact source and lockfile.

### CRITICAL limitation

**AIG v0.2.0 is not the multi-step workflow engine.** It supports one trusted `SIDE_EFFECT` tool per Runtime composition, a *single* step, default 5-second executor deadline (optional carefully reviewed maximum 15 seconds), fail-closed Unknown, exact Plan Approval **separate from** Action Authorization. It does not sandbox malicious code and does not provide product authentication.

### Allowed AIG operation: `enqueue_incident_trial/1`

- Compile exactly one Plan Action targeting an immutable **local incident-run queue**.
- Strict fixed-flat tool schema: consumer `trial_id` (distinct from AIG `run_id`), fixture/scenario identities and digests, manifest digest and policy profile. Installed v0.2.0 supports bounded scalar fields and trusted string patterns, **not `enum`/`const`**. ADR-009 defines the exact closed six-field schema and semantic checks.
- The trusted executor validates all identities again and performs **one short local durable queue insertion** under default 5-second executor budget. It returns a receipt **only proving queue admission** (not completed remediation).
- The effect store atomically binds **AIG effect key + complete payload digest + receipt id + job id**, enforcing uniqueness. Same key/payload returns the original recorded receipt; same key/different payload fails; unproven commit becomes `Unknown` with **no automatic redispatch**.
- Dispatch runs through **Plan → persistent Run → actual authenticated human Approval → Action admission → independent Authorization → durable claim → short enqueue effect → queue receipt**. Two separate human steps can be present in UI; never treat a model or scripted sample as a real approver.
- **After confirmed AIG success**, a trusted releaser verifies the public Action state and exact queue receipt before changing a committed job from HELD to READY. The product-owned worker independently runs the longer bounded experiment, with its own timeline/result. A lost-acknowledgment/Unknown Action must not release a held job. The worker cannot change the verified approved manifest; no signing claim is made in v1.
- The short AIG operation MUST NOT await the 30–180-second sandbox job. It must not launch detached work inside the AIG executor. The **trusted worker process** polls a separately durable product job queue.
- If AIG Action is `Unknown`, perform **read-only status inspection**; do not auto-create another AIG Action or blindly retry the enqueue. If a worker crashes after dispatch, classify the job `INCONCLUSIVE / UNKNOWN`, quarantine resources, inspect and clean safely; never auto-repeat an uncertain effect.

### Consumer-owned execution versus AIG scope

Within the *already authorized* bounded sandbox trial, the consumer worker may coordinate multiple deterministic, sandbox-confined actions: replay, patch application, test execution, probe, cleanup. These are product-level steps and **must not be described as independent AIG-authorized Side Effect actions**. No third-party irreversible effects are in scope. If later introducing production changes, payments, GitHub writes or external deployment, they require newly scoped human authorization, and likely an independently reviewed architecture.

### Product-specific AGENTS addendum (merge, don't replace upstream text)

At the bottom of root `AGENTS.md`, append concise references:

```markdown
## Faultline Proof competition-specific overlay
- Read `docs/MASTER_DESIGN.md` before proposing changes.
- Respect pre-kickoff originality boundary and latest lablab rules.
- All LLM calls for actual competition agent behavior go through Vultr Serverless Inference.
- AIG only authorizes ONE durable sandbox-trial enqueue; it is not a multi-step executor.
- No real production, external repo mutation or arbitrary user code in MVP.
- No Docker socket, network credentials, host paths or cloud tokens inside the sandbox.
- Evidence status must be derived from deterministic checks; never fabricate PASS.
- Never commit, push, deploy, purchase infrastructure, or make real cloud calls without explicit authorization.
```

---

## 7. Orchestration workflow and state contracts

### Product run states

`DRAFT → PATCH_PROPOSED → PLANNED → AWAITING_APPROVAL → APPROVED → AWAITING_AUTHORIZATION → AUTHORIZED → HELD → READY → PREPARING → BASELINE_RUNNING → CANDIDATE_RUNNING → VERIFYING → CLEANING → {PROVEN_FOR_THIS_SCENARIO | REJECTED | INCONCLUSIVE}`

- Every state transition persists a monotonic per-run sequence and timestamp.
- Terminals are immutable, unless a clearly documented **new run** is created. An abandoned worker lease becomes `INCONCLUSIVE`, not a silent replay.
- AIG Action status is **separate**: `Succeeded` means enqueue verified; an incident trial can subsequently fail, reject, or be inconclusive.
- Cancel only terminates tasks the worker can provably terminate, and always triggers safe cleanup. Cancellation does not imply external effects were undone.

### Fixed workflow (not unrestricted model tools)

1. **Analyze:** retrieve bounded fixture logs and incident metadata; Vultr LLM proposes an exact bounded candidate patch. Trusted code validates its bytes and freezes the manifest before the persistent AIG Plan is created.
2. **Approve:** human reviews exact Plan + actual candidate diff + immutable manifest + trusted target, then explicitly approves and separately authorizes enqueue.
3. **Queue:** AIG's single trusted executor inserts one exact, fingerprinted job with durable receipt.
4. **Baseline:** trusted runner starts a clean fixture and runs the frozen reproduction test, saving original metrics and evidence.
5. **Patch:** materialize only the already approved diff against the frozen source. Recheck paths, literal-config shape and tree hashes. **No new patch generation or replacement inside an approved trial.**
6. **Candidate:** runner creates a separate isolated candidate container and runs the same trusted tests/probe. A failed candidate remains visible; any model-guided revision requires a new trial, Run, Approval and Authorization.
7. **Verify:** deterministic evaluator compares requests, status codes, error counts, p95, invariant tests, patch scope, sandbox metrics, isolated env and cleanup claims. Explain delta with LLM only after hard evaluation.
8. **Clean:** terminate containers, remove network and temporary job workspace, verify observed cleanup; persist lifecycle receipts.
9. **Publish:** Evidence Passport with explicit evidence grades, limits, patch, replay settings, result, and a *human review required* deployment recommendation.

### Model trust rule

LLM output is **data**, never an authority source. The model cannot set allowed execution commands, host paths, docker options, deployment targets, risk profile, hidden benchmark thresholds, approval status or artifact URLs.

---

## 8. Sandbox threat model & enforceable controls

**Assets:** Vultr VM host, Docker daemon, trusted control plane, AIG gate ledger, Vultr key, fixture/test integrity, evidence, spend and availability.

**Untrusted:** user-visible incident descriptions, fixture log lines, model text and generated patches, source code in sandbox, public input, any artifact path request.

**Attacker objectives:** host file reads/writes, credential exfiltration, unsanctioned network access, fork bombs, memory exhaustion, path traversal, editing verifier tests, duplicate task execution, prompt injection, forged PASS/report, overspend.

### Mandatory controls

- Run sandbox as non-root with no-new-privileges, drop all ambient capabilities, seccomp profile, pids/memory/cpu/time caps; prefer rootless Docker or stronger isolation if supported and tested. **Do not claim gVisor unless actually deployed.**
- Root filesystem read-only where feasible; ephemeral writable `/tmp`/`/workspace` with bounded tmpfs or controlled ephemeral volume.
- No host filesystem mount containing secrets. Never mount Docker socket, SSH agent, AWS creds, Vultr creds or host home directory inside sandbox.
- No public internet egress. For service/probe interaction use an isolated, per-job Docker `internal` network or equivalently enforced namespace; allow only intended service ↔ probe communications. Check connectivity rather than asserting it.
- Sandbox receives no LLM API key. Trusted orchestrator calls Vultr inference.
- Fixed trusted test commands, with program/args arrays (not shell concatenation), capped stdout/stderr, exception-safe timeouts; never execute model-provided shell text directly.
- Patch allowlist by canonical resolved path within sandbox fixture. No symlink escape, absolute paths, `/proc`, `/sys`, `/etc`, test harness modification, or `../` traversals.
- Every sandbox has TTL, resource quota and cleanup policy, **and an observed cleanup record**. Distinguish unsuccessful cleanup as `INCONCLUSIVE`/guard failure.
- Public API has per-session/global run limits, max concurrent containers, fixed built-in scenarios, bounded file/artifact reads and authenticated human Approval/Authorization. Public read-only mode is acceptable when live mutation endpoints cannot be made safe.
- Trusted runner's Docker access is a privileged attack surface: bind its control API locally, keep it separate from public API runtime, validate every request, and avoid internet-facing control ports.
- Enforce explicit model token/attempt caps and Vultr spend alarms. Kill orphaned resources by tagged job ID only; **never delete unrelated Docker containers or existing Kind clusters**.

### Required real containment experiments

**CT-01 Host-only marker:** create a harmless host marker **outside all sandbox mounts**. Attempt to access a known synthetic marker path from within a sandbox; expect absent/inaccessible; afterward verify original host marker hash remains unchanged. No real secrets used.

**CT-02 Timeout:** run a controlled infinite-loop fixture *inside an isolated sandbox*, enforce deadline, observe process/container termination and residual-resource cleanup, without affecting host.

**CT-03 Policy/path rejection:** force a model-generated patch targeting `tests/`, an absolute host path or `../`; validator rejects before applying; record structured reason.

**CT-04 Poisoned log:** malicious instruction placed in untrusted diagnostic log does not obtain host credentials, bypass Approval, or alter trusted verifier conditions. If model complies in text, validator must still block effect and report an unsafe proposal.

**Evidence standard:** record command identity, container ID, image digest, exit code, resource/timeout observation, timestamps and post-cleanup inspection. These are test observations, **not formal proof of universal host compromise impossibility**.

---

## 9. Counterfactual verification and Evidence Passport

### Objective metrics

Per run, store the *raw sample sizes* and conditions; metrics without denominators are insufficient.

- `total_requests`, `http_5xx_count`, `error_rate = errors / total_requests`.
- `p50_ms`, `p95_ms`, maximum timeout count, functional-test passed/failed.
- `baseline_reproduced`: predetermined degradation condition met under frozen scenario.
- `candidate_recovered`: predetermined recovery thresholds met **on the same scenario**.
- `no_regressions`: named unaffected endpoints and invariants still pass.
- `patch_scoped`: all edits constrained to allowlist, harness digests intact.
- `containment_observed`, `cleanup_observed`: pass only on direct, persisted trusted checks.

The Phase 0 targets (qualify before candidate evaluation; see the complete fixture specification):

- Baseline exactly 200 quote probes, >= 20% failed requests and retry amplification >=1.5.
- Candidate exactly 200 comparable quote probes, <= 1% failed requests and amplification <=1.30.
- No known healthy endpoint regression; `pytest` expected cases all pass.
- Candidate p95 <=350 ms, with fixed open-loop traffic, seed and independent upstream measurements. Targets are NOT observed results.

### Deterministic decision (illustrative)

```python
def trial_verdict(e):
    if e.proven_policy_or_security_violation:
        return "REJECTED"
    if not e.evidence_complete or not e.cleanup_observed:
        return "INCONCLUSIVE"
    if not e.baseline_reproduced or not e.scenarios_equivalent:
        return "INCONCLUSIVE"
    if not e.patch_scoped or not e.security_controls_passed:
        return "REJECTED"
    if e.candidate_recovered and e.no_regressions and e.tests_passed:
        return "PROVEN_FOR_THIS_SCENARIO"
    return "REJECTED"
```

**Causal honesty:** one controlled experiment provides evidence only for this fixture, scenario and sample. Do not claim a production SLA guarantee. If baseline not reproducible, never label candidate successful.

### Evidence Passport v1 JSON shape

```json
{
  "schema": "faultline-evidence-v1",
  "run_id": "uuid",
  "fixture": {"id": "retry-storm-503", "revision": "v1", "source_sha256": "...", "image_digest": "..."},
  "scenario": {"id": "replay-v1", "seed": 1024, "probe_spec_sha256": "..."},
  "governance": {"plan_digest": "...", "approval_event_id": "...", "authorization_event_id": "...", "aig_enqueue_receipt_id": "..."},
  "model": {"provider": "Vultr Serverless Inference", "model_id": null, "request_count": null},
  "execution": {"baseline_container_id": "...", "candidate_container_id": "...", "sandbox_profile": "isolated-v1"},
  "baseline": {"status": "NOT RUN", "requests": null, "errors": null, "p95_ms": null},
  "candidate": {"status": "NOT RUN", "requests": null, "errors": null, "p95_ms": null},
  "patch": {"sha256": "...", "changed_paths": ["service/config.py"]},
  "guards": {"patch_scope": "NOT RUN", "host_marker": "NOT RUN", "timeout": "NOT RUN", "cleanup": "NOT RUN"},
  "artifacts": [{"kind": "baseline_log", "sha256": "...", "relative_path": "logs/baseline.txt"}],
  "decision": "NOT RUN",
  "limitations": ["No production deployment", "One fixed scenario; no universal security proof"]
}
```

**This is a schema illustration, not an execution manifest or benchmark. Actual identity/digest values must come from execution; absent metrics are null, never fabricated zeros.**

Compute artifact SHA-256 over actual bytes and a canonical manifest digest. If adding a trusted signer, document key custody, signature verification, and exact threat model. A plain hash alone does **not** prove the host did not lie or that isolation is cryptographically attested.

Export a self-contained ZIP containing patch.diff, summary.md, manifest.json, baseline/candidate metrics JSON, test stdout, and constrained container inspection/lifecycle evidence. All files omit secrets and redact private values.

---

## 10. Typed API contract (MVP)

```text
GET    /api/healthz                  -> status, build_sha, vultr_inference_configured:boolean (no secrets)
GET    /api/incidents                -> fixed manifest-backed incidents
GET    /api/incidents/{fixture_id}   -> sanitized incident details, replay protocol
POST   /api/trials/draft             -> create trial with fixture_id, idempotency_key
GET    /api/trials/{run_id}          -> trial state, event sequence, canonical URLs
POST   /api/trials/{run_id}/plan     -> Vultr LLM-assisted bounded Plan
POST   /api/trials/{run_id}/approve  -> authenticated explicit Plan approval, exact digest
POST   /api/trials/{run_id}/authorize -> independent Action Authorization
POST   /api/trials/{run_id}/enqueue  -> AIG single-tool authorized durable enqueue
GET    /api/trials/{run_id}/events   -> SSE with strictly increasing sequence IDs
GET    /api/trials/{run_id}/metrics  -> baseline/candidate samples, denominators
GET    /api/trials/{run_id}/proof    -> provenance, checks, verdict and limitations
GET    /api/trials/{run_id}/artifacts/{artifact_id} -> allowlisted downloads
GET    /api/trials/{run_id}/export   -> bounded signed? ZIP; sign only if actually implemented
```

`POST` requires CSRF/session protections as relevant, documented error envelope and idempotency keys. Scope auth by run and actor. Reject forged run IDs, stale plan digests, mismatched operator, duplicate authorization, incompatible trial manifest and attempts to modify completed work.

### Illustrative API error envelope

```json
{
  "code": "APPROVAL_REQUIRED",
  "message": "The exact plan digest must be explicitly approved before action authorization.",
  "run_id": "...",
  "retryable": false
}
```

Do not expose traceback, provider keys, capability tokens, full Docker inspection data containing host internals, or unsafe arbitrary file reads via browser routes.

---

## 11. Persistence and idempotency schema

Use separate SQLite WAL stores (single VM deployment). Suggested tables:

```text
consumer.trials(run_id PK, fixture_id, actor_id, manifest_digest, plan_digest,
                state, created_at, updated_at, version, verdict)
consumer.trial_events(run_id, seq, type, payload_json, created_at, PRIMARY KEY(run_id,seq))
consumer.enqueue_effects(effect_key UNIQUE, payload_digest, run_id UNIQUE,
                         receipt_id UNIQUE, committed_at)
consumer.jobs(job_id PK, run_id UNIQUE, effect_key UNIQUE, status,
              claimed_at, worker_id, started_at, completed_at, attempt_count)
consumer.model_calls(call_id PK, run_id, model_id, status, latency_ms,
                     input_tokens, output_tokens, estimated_cost_usd, request_digest)
consumer.artifacts(artifact_id PK, run_id, kind, sha256, byte_size,
                   canonical_relative_path, created_at)
consumer.probes(run_id, variant, scenario_digest, count, errors, p50_ms, p95_ms,
                raw_artifact_id, PRIMARY KEY(run_id,variant))
consumer.containment_checks(run_id, check_id, result, details_artifact_id,
                            PRIMARY KEY(run_id,check_id))
```

Keep private AIG DB separate. Document schema migrations. No automatic queue replay of jobs with uncertain execution. Atomic insertion and effect-key conflict handling need real concurrent tests and process-crash cases. Fail closed when the original worker status cannot be proven.

---

## 12. Technology choices

| Layer | Decision | Reason |
|---|---|---|
| Frontend | React + TypeScript + Vite (or Next.js only if it remains thin) | Ship real dashboard quickly; avoid duplicate Node backend logic |
| UI | Tailwind + accessible components + Recharts | Excellent SRE console/metrics comparison |
| Backend | Python 3.13 + FastAPI + Pydantic v2 | Direct AIG public Python integration |
| Agent | Explicit finite-state orchestrator, strict JSON response schema | More controllable than general multi-agent runtime |
| LLM | Vultr Serverless Inference OpenAI-compatible client | Official mandatory provider; feature-test actual model |
| Governance | `agentic-intent-gate` v0.2.0 pinned Git commit | Reuse durable Plan/Approval/Authorization/Action capabilities |
| Execution | Docker ephemeral containers on Vultr VM | Official recommended Pattern A |
| Evidence | SQLite WAL + hash-addressed artifacts + ZIP export | Transparent reproducible proof workflow |
| Service fixture | Small Python FastAPI toy service + scripted mock upstream | Real fault/probe mechanics, controlled repeatability |
| Tests | pytest + httpx + Playwright + TypeScript tests | Verify backend, workflow, browser and security paths |
| Deployment | Vultr VM, HTTPS reverse proxy, systemd or Compose | Central Vultr-controlled architecture |

**Model selection:** discovery-based configuration; perform live tests for JSON validity, patch-quality and observed response model ID. Never pin an unverified advertised model name or silently fall back to another provider. A model call to a non-Vultr provider in the shipped agent flow is a compliance failure.

**Cost protection:** one global active trial in v1, token/request caps, no automatic model retries, and server-owned admission ceilings. Actual provider billing caps/alerts and prices must be verified before provisioning; local caps are not a guaranteed provider hard spend stop.

---

## 13. Repository layout

```text
faultline-proof/
├── AGENTS.md                    # EXACT upstream consumer policy + project overlay
├── README.md                    # Public pitch, real links, evidence and status
├── LICENSE                      # MIT (verify dependencies and fixture licenses)
├── pyproject.toml               # Python 3.13 + exact pinned AIG dependency
├── uv.lock
├── package.json                 # Only if top-level workspace tooling needs it
├── .env.example                 # Placeholder keys only
├── .gitignore
├── docs/
│   ├── MASTER_DESIGN.md         # This document
│   ├── REQUIREMENTS_TRACEABILITY.md
│   ├── THREAT_MODEL.md
│   ├── EVIDENCE_SCHEMA.md
│   ├── DEPLOYMENT_RUNBOOK.md
│   ├── DEMO_SCRIPT.md
│   ├── ORIGINALITY_AND_REUSE.md
│   └── PHASE_REPORTS/
├── apps/
│   └── web/                     # React/TS incident console
├── src/faultline/
│   ├── api/                     # FastAPI, auth/session, SSE
│   ├── domain/                  # models, states, verdicts
│   ├── inference/               # Vultr-only provider + output validation
│   ├── governance/              # thin AIG consumer integration
│   ├── orchestration/           # consumer-owned finite run workflow
│   ├── sandbox/                 # runner RPC, image builds, cleanup
│   ├── evaluation/              # immutable scenario and verifier
│   ├── evidence/                # receipts, artifacts, hashes, export
│   └── persistence/             # migrations and repositories
├── fixtures/
│   ├── retry-storm-503/
│   │   ├── manifest.json
│   │   ├── service/
│   │   ├── trusted-tests/
│   │   └── scenario/
│   └── suspicious-log-injection/
├── tests/
│   ├── unit/
│   ├── contract/
│   ├── integration/
│   ├── security/
│   ├── recovery/
│   └── e2e/
├── infra/
│   ├── vultr/
│   ├── docker/
│   └── deployment/
├── scripts/
│   ├── verify-aig-pin.py
│   ├── run-local-demo.py
│   ├── run-sandbox-security-suite.py
│   └── verify-evidence.py
└── submission/
    ├── cover.png
    ├── deck.pdf
    ├── demo-video.mp4
    └── SUBMISSION_CHECKLIST.md
```

Do not create empty facade modules just to imitate this tree. Implement only files needed for each phase; evolve the structure when measured evidence demands it.

---

## 14. Phase gates and definition of done

### PRE-KICKOFF: Research/Design/Compliance (2026-10-19 through kickoff)

**Allowed pending rule confirmation:** competition enrollment, Vultr account and billing research, read docs, run public sample APIs only with explicit permission, local architecture design and source attribution, choose fixtures and threat model, prepare local toolchains. **Do not prebuild the competition-specific core agent, tested implementation or submission before the allowed window unless official rules explicitly permit it.** Recheck legality of pre-existing scaffolding.

Deliverable: frozen concept, source links, validated AIG API limitations, contest requirements checklist, competing-product differentiation, budget and proof plan. Target status: `DESIGN_READY`, not `BUILD_PASS`.

### P0 — Infrastructure reality (kickoff day, NZDT Nov 4)

- Provision authorized Vultr VM, HTTPS/public test route, secret storage and resource budget.
- Confirm live Serverless Inference auth/model via an actual response and actual model ID.
- Harden a test sandbox and execute a harmless command on Vultr, recording container/image IDs and cleanup.
- Verify pinned installed AIG dependency and basic integration tests.
- **Gate:** backend and sandbox really execute on Vultr; public browser can reach the app; no secret exposures.

### P1 — Executed incident baseline (Nov 4–5)

- Build one actual incident fixture and freeze replay scenario.
- Show real baseline failure: >= documented sample count and logs/metrics artifact.
- Render incident UI from actual API (not client demo data).
- **Gate:** deterministic failure reproduction and evidence available via public UI.

### P2 — Real governed agent repair (Nov 5–6)

- Vultr model diagnosis + bounded candidate diff; closed patch validator.
- Real user approval and separate authorization; AIG durable queue receipt under 5s.
- Trusted worker executes actual baseline/candidate using the approved frozen patch; revisions require a fresh trial and consent.
- **Gate:** end-to-end execution produces actual diff, tests and raw comparison; AIG receipt never conflated with remediation verdict.

### P3 — Containment + recovery fault injection (Nov 6–7)

- CT-01 marker / CT-02 timeout / CT-03 forbidden patch / CT-04 poisoned log.
- Crash/duplicate/conflict/Unknown and cleanup tests, strict lifecycle visibility.
- **Gate:** malicious proposals cannot affect host or trusted runner in tested scenarios; all failed checks visible and not dressed up as PASS.

### P4 — Experience, evidence and deployment hardening (Nov 7)

- Crisp guided walkthrough, SSE stream, baseline/candidate comparison, Evidence Passport downloads.
- Public UX regression, load/concurrency limits, budget alarms, reliability of startup/restart.
- **Gate:** second-browser evaluation can reproduce golden path; no secret leaks, stale fake data, unreadable errors.

### P5 — Submission lock (Nov 8 NZDT)

- Stable deployed URL, public source+MIT+accurate README, instructions reproducible.
- Video <= 5 minutes and <= 300 MB per general lablab guidelines (verify current event submission UI), with actual containment moment.
- Pitch deck, cover, exact submission fields, third-party attribution, screenshot/recording permissions, evidence hashes.
- Video deliberately features both successful verified recovery **and** a blocked unsafe attempt.
- **Gate:** evaluator can click a working public URL and independently see true artifacts and honest failure states. Submit well before Nov 9 11:00 NZDT.

### Cut order under time pressure

Cut in this order: extra incident C → fancy animation → PDF export (keep JSON/ZIP) → user accounts beyond gated demo → multiple LLMs → second incident B as full independent product flow (still retain one containment test) → model repair second retry. **Never cut** Vultr VM deployment, Vultr inference, public demo, actual executable result, sandbox containment, core SRE comparator, honest evidence, final video/slides.

---

## 15. Objective release gates / test matrix

| ID | Test | Required evidence | Gate |
|---|---|---|---|
| C-01 | All LLM calls on Vultr | redacted endpoint/config + actual model response IDs | MUST |
| C-02 | Backend on Vultr VM | public URL + host/service info + deployment checks | MUST |
| C-03 | Real sandbox execution | container IDs, commands, timestamps, stdout and cleanup | MUST |
| G-01 | Exact Plan / human Approval / separate Authorization | persistent, correlated event IDs | MUST |
| G-02 | Wrong binding/scope/plan/stale consent denied | contract tests with durable state | MUST |
| G-03 | Duplicate/concurrent enqueue no second queue effect | unique effect key, DB assertions | MUST |
| G-04 | Unknown effect fails closed | fault injection, no automatic redispatch | MUST |
| R-01 | Broken baseline reproducibly fails | raw N probes + hashes | MUST |
| R-02 | Model-proposed patch is real and scoped | recorded model response + diff validator + file hash | MUST |
| R-03 | Patched candidate really tested | raw N probes + pytest logs + comparison | MUST |
| R-04 | No fabricated PASS | negative tests and deliberate verification failures | MUST |
| S-01 | Host-only marker not accessible | sandbox result and host hash before/after | MUST |
| S-02 | Infinite loop hits resource/time bound | timeout/termination/cleanup records | MUST |
| S-03 | No sandbox secret/socket mount | container inspection + mount/env audits | MUST |
| S-04 | Poisoned logs cannot grant privileges | rejected actions and no host side effects | MUST |
| D-01 | Live browser end-to-end | Playwright / second-browser capture | MUST |
| D-02 | Submission completeness | valid demo, public repo, deck, video, cover | MUST |
| Q-01 | Cost & latency measurement | observed model/job timing and token/cost log | SHOULD |
| Q-02 | Artifact integrity verification | offline verify-evidence script | SHOULD |
| Q-03 | Repeatable 3-run fixture benchmark | same scenario/seed, no cherry-picking | SHOULD |

**Do not set all requirements to PASS from test counts alone.** Each PASS requires linked evidence. Security guarantees are explicitly bounded to tested configurations.

---

## 16. Real demonstration script (4:30 target)

**00:00–00:25 — The pain.** "AI can suggest a fix for an outage. It cannot be trusted merely because it sounds confident." Show red incident timeline and broken endpoint.

**00:25–01:00 — Diagnosis and governance.** Ask model to triage. Show actual Vultr call provenance, review the changed paths and plan digest. Click **Approve Plan** then **Authorize Trial**; explain these are distinct decisions.

**01:00–02:05 — The executed repair.** Start the approved sandbox job. Show real baseline replay 5xx, the frozen model-generated diff, test output and candidate probe results. A failed candidate is retained; a revised patch needs a new trial and consent. Use the detailed timing in `docs/DEMO_SCRIPT.md` for recording.

**02:05–02:50 — Counterfactual evidence.** Split-screen baseline versus patched candidate, fixed seed/test specification, numerator/denominator, p95, regression checks and `PROVEN_FOR_THIS_SCENARIO` (only if actually measured).

**02:50–03:35 — Containment moment.** Trigger the prepared benign synthetic host-marker read attempt or controlled infinite-loop case inside isolated sandbox. Show failure/termination plus VM host-marker integrity and lifecycle cleanup evidence. Never run destructive host-side commands.

**03:35–04:15 — Passport + outcome.** Open complete provenance, real patch/test artifacts and honest limitations; export bundle. Emphasize **not deployed to production** and reviewable next action.

**04:15–04:30 — Business value.** "From plausible AI advice to a measurable, isolated recovery experiment that an on-call engineer can trust enough to review." Display actual public URL and repo.

**Filming:** record a fresh real run; no fake terminal output, invented counts or cut-and-paste synthetic logs masquerading as real. Optional voice-over after silent capture, with accurate on-screen captions. Validate accessibility and no credentials in captures.

---

## 17. Submission and judges' alignment

| Judging dimension | Why this product can score | Evidence to show |
|---|---|---|
| Application of Technology | Real Vultr inference + stateful cloud execution + resource-contained sandboxes | live model provenance, VM deployment, container lifecycle |
| Presentation | Visually obvious red→green before/after and one unforgettable blocked-unsafe moment | simple story, split-screen chart, <5 minute video |
| Business Value | SRE incident response, reduced human verification burden, safe candidate evaluation | measurable degradation and recovery, reproducibility, reviewable artifact |
| Originality | Counterfactual incident twin + governance-enforced launch + conservative proof language | same-seed comparator, policy denials, Evidence Passport |

**Defensibility:** this is not "patch generated" or "container spawned". The differentiator is **governed, bounded, reproducible incident-resolution evidence**. Keep original metrics and actual denied outcomes central in every demo.

### Originality and shared-core attribution

- The repo uses a previously released MIT Python AIG runtime. Attribute its author/repo/release/pinned commit and document unchanged external-core functionality separately from hackathon-built product features.
- Keep a `docs/ORIGINALITY_AND_REUSE.md` table with columns: component, original source/date, existing vs competition-developed, license, evidence link.
- Do not transplant code wholesale from other entries or rely on an unlicensed third-party repo.
- Review the official rule book/organizer clarification if pre-existing reusable runtime eligibility remains uncertain. If not permitted, stop and report the conflict: root AGENTS mandates the pinned AIG dependency. Removing it or redesigning governance requires explicit separately reviewed authorization; never hide reused code.

---

## 18. Engineering decision records

**ADR-001 — Use a bounded incident domain rather than a general-purpose coding agent.** Improves originality, business value, testability and demo coherence.

**ADR-002 — AIG gates queue admission only.** Its synchronous single trusted tool with <=5s default deadline cannot truthfully represent a multi-minute incident remediation chain. Queue receipt != candidate success.

**ADR-003 — Reference production-like service is never mutated.** Only experiment sandboxes are affected; output is a reviewable patch and recommendation. No fake deploy success.

**ADR-004 — Deterministic evaluator owns verdict.** LLM may explain results but never declare proof PASS.

**ADR-005 — One Vultr VM + finite hardened containers.** Satisfies event infrastructure requirements with manageable delivery risk. K8s/gVisor are optional only after real validation.

**ADR-006 — Fail-closed for ambiguous dispatch/recovery.** Do not retry uncertain effects or claim exactly-once behavior.

**ADR-007 — Evidence is test-bounded.** Artifact hashes + isolated execution observations do not equal cryptographic attestation or guaranteed no host escape.

**ADR-008 — Public demo is constrained.** Fixed fixtures, explicit human interaction, rate limits, budgets and no open execution API.

---

## 19. Operating instructions for coding agents

1. Read root `AGENTS.md` and **this** `docs/MASTER_DESIGN.md` before modifying the repository.
2. Read the pinned AIG handoff, adapter guide and actual `examples/consumer/app.py`, verify installed API. Never invent private/public Runtime methods.
3. Verify official hackathon eligibility and kickoff timing before competition-specific implementation. Before kickoff, work only on permitted design/research and environment preparation.
4. Work in **one gated phase per iteration**. Write `docs/PHASE_REPORTS/P{n}.md` with current code diff, real tests, evidence paths, status `PASS | PARTIAL | BLOCKED` and next highest-value action.
5. Before every network-mutating action, infrastructure spend, Git commit/push, deployment or test with third-party side effects, request explicit user permission if not previously provided in the current instruction.
6. Use synthetic local fixtures for offline tests by default. Once authorized, real Vultr calls must record redacted proof of service/model selection.
7. Do not embellish documentation with fabricated URLs, credentials, timestamps, numbers, completed functionality, or screenshots.
8. Preserve strong containment and human approval even if shortening the feature set under deadline pressure.
9. Never turn this into an AIG fork, general multi-tool agent, huge orchestration framework or Kubernetes-platform rewrite.
10. At every phase end, recommend **Codex Sol** and reasoning effort for the next phase: High for implementation; Extra High for architecture, AIG trust boundary, sandbox security, or difficult debugging, when available. Use the VS Code Codex plugin.

---

## 20. Final win condition

The project counts as a **competition-ready credible submission**, not an award guarantee, only when:

- A member of the public can visit the real Vultr-hosted web app.
- An evaluator sees a real incident whose baseline failure is independently observed.
- Real Vultr Serverless Inference proposes a real candidate code/config patch.
- The trusted governance flow approves and authorizes exactly one bounded sandbox trial before the consumer worker acts.
- Baseline and candidate actually execute with the **same replay scenario** in isolated Vultr sandboxes.
- The verifier records measured recovery, no regression, and honest uncertainty with raw artifacts.
- The video shows actual containment and successful lifecycle teardown.
- GitHub, licenses, README, architecture, demo URL, <=5min video, deck, cover and exact contest form are completed by the submission cutoff.

**North-star sentence:** *Faultline does not ask you to trust an agent's answer. It gives you an isolated experiment and the evidence needed to challenge it.*

---

## Primary research references (as checked 2026-10-19)

- [Official Vultr Agent Rush challenge and judging](https://lablab.ai/ai-hackathons/vultr-hackathon)
- [Official live UTC kickoff / submission clocks](https://lablab.ai/ai-hackathons/vultr-hackathon/live)
- [lablab submission format and video guidance](https://lablab.ai/ai-articles/hackathon-guidelines)
- [Vultr Serverless Inference docs](https://docs.vultr.com/products/compute/serverless-inference)
- [Vultr inference chat endpoint/tool calls](https://docs.vultr.com/products/compute/serverless-inference/management/usage/chat)
- [Competitor: PatchProof](https://lablab.ai/ai-hackathons/vultr-hackathon/patchproof)
- [Competitor: Airlock](https://lablab.ai/ai-hackathons/vultr-hackathon/airlock)
- [AIG dependency instructions](https://github.com/miku-wwl/agentic-intent-gate/blob/main/docs/AGENTS-dependence.md)
- [AIG v0.2.0 consumer handoff](https://github.com/miku-wwl/agentic-intent-gate/blob/main/docs/V0.2.0-CONSUMER-HANDOFF.md)
- [AIG v0.2.0 adapter guide](https://github.com/miku-wwl/agentic-intent-gate/blob/v0.2.0/docs/ADAPTER_GUIDE.md)
