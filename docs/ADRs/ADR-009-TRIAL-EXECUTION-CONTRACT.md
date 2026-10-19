# ADR-009 — Freeze exact trial contents and hold admission until confirmed

Date: 2026-10-19. Status: **Design decision for implementation; NOT IMPLEMENTED**.

This narrows Master Design sections 6–11; it preserves the single AIG effect and separate worker. Scope: v1, one fixed incident, one candidate, one worker, one active trial. Extended AIG budgets, automatic repair retries, distributed execution and production changes are excluded.

## 1. Resolve the two approval races

The previous workflow described an early proposal but generated/revised the executable patch after approval. V1 instead obtains the real Vultr diagnosis and candidate **before approval**, validates it, stores its exact bytes, and freezes the manifest. The human sees the actual diff, policy, measurements to be collected and limits. Any changed patch, scenario, thresholds or manifest requires a new trial, new Run, fresh Approval and separate Authorization. The worker cannot obtain an executable replacement patch. Model explanations may annotate observed results only.

Queue COMMIT and AIG finish are separate transactions. A job therefore enters `HELD`, not runnable. A trusted control-plane releaser reads `runtime.gateway.get(action_id, principal)` and requires `Succeeded`, an exactly matching receipt reference/specification, and the immutable consumer Run/Action/trial links. It then atomically changes `HELD -> READY` with a persisted release observation. A worker can claim only `READY`.

If COMMIT succeeded but the adapter's acknowledgment was lost, AIG may be `Unknown` with a real held queue row. **It must never run.** Restart can reread public Action state and release a proven `Succeeded` job; that is read-only status recovery followed by consumer bookkeeping, not re-execution or rewriting an Unknown Action. Unknown/interrupted/unavailable state remains held/quarantined. No direct read/write of AIG tables, private APIs, forged success or automatic new Action.

## 2. Trusted identities and argument schema

Exactly one startup binding:

| Field | Frozen v1 value |
|---|---|
| tool_name / tool_version | `enqueue_incident_trial` / `1` |
| adapter_id | `faultline-local-queue` |
| binding_revision | `trial-enqueue-v1` |
| target | `faultline-trial-queue` |
| execution_scope | Fresh canonical UUIDv4 provisioned once in private host configuration; retained on restart |
| policy revision | `faultline-policy-v1` |
| adapter budget | Default 5 seconds, no extended suffix |

Scope is deployment identity, not a new per-request random value. Store the entire binding, policy, gate/effect-store identity and schema digest before startup. Missing configuration fails startup; never silently provision replacement identities over existing state.

The following is a **documentation schema**. Installed public `ToolCapability` construction and Plan parsing passed the Phase 0 structural checks; consumer manifest/owner semantic validation remains NOT IMPLEMENTED:

```json
{
  "type": "object",
  "additionalProperties": false,
  "required": ["trial_id", "fixture_id", "scenario_id", "scenario_digest", "manifest_digest", "policy_profile"],
  "properties": {
    "trial_id": {"type": "string", "minLength": 36, "maxLength": 36, "pattern": "^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$"},
    "fixture_id": {"type": "string", "minLength": 15, "maxLength": 15, "pattern": "^retry-storm-503$"},
    "scenario_id": {"type": "string", "minLength": 15, "maxLength": 24, "pattern": "^(retry-storm-503|suspicious-log-injection)$"},
    "scenario_digest": {"type": "string", "minLength": 64, "maxLength": 64, "pattern": "^[0-9a-f]{64}$"},
    "manifest_digest": {"type": "string", "minLength": 64, "maxLength": 64, "pattern": "^[0-9a-f]{64}$"},
    "policy_profile": {"type": "string", "minLength": 8, "maxLength": 8, "pattern": "^trial-v1$"}
  }
}
```

`trial_id` is consumer-owned; it is not the AIG `run_id`. AIG creates the Run after the manifest is frozen. All arguments are supplied by the trusted manifest lookup, never copied from browser/model authority fields. The semantic rule rechecks canonical UUIDv4, allowed scenario/fixture mapping, existing immutable manifest, input/scenario digests, policy and owner. Executor repeats these checks and exact six-field binding/`EXTERNAL_PAYLOAD_REVISION` validation.

The manifest is a closed versioned object (`faultline-trial-manifest-v1`) with: trial ID; sanitized diagnostic-input digest; source revision/tree digest; base OCI digest; exact patch digest and byte count; candidate tree digest; trusted config-parser digest; scenario vector/replay/evaluator/test digests; policy/profile; all limits; metric thresholds; model response/call evidence reference and digest; approved containment probes. No secrets, mutable URLs or model commands. A separate immutable governance link records AIG Run, exact stored Plan digest, Approval version/event, Action, Authorization and product human-event references after they exist. Do not hash future IDs into a self-referential manifest.

Canonical manifest encoding: recursively sorted ASCII keys, UTF-8, no whitespace, no BOM, no floats, duplicate keys or non-finite values; LF-normalized source files only before their identity is frozen. Hash actual patch/artifact bytes without later normalization. AIG's `spec.payload_digest()` remains the authority for **AIG** payload identity; the consumer manifest hash is separate.

## 3. Planning, consent and authorization

1. Authenticated operator selects an allowlisted fixture. Server checks quotas before a bounded Vultr call. Planning inputs include clearly marked untrusted diagnostic text; output is a constrained repair proposal.
2. Trusted code validates the real response, patches only the permitted config literals in a disposable data workspace without importing/executing candidate Python, computes identities and persists the frozen manifest. No sandbox trial starts here.
3. A consumer `ModelProvider.generate_plan` supplies the one-step Plan envelope based on this recorded model proposal and trusted manifest mapping. The earlier Vultr call is separately attributed; do not claim an additional LLM call from serializing the envelope. This also avoids trying to fit a slow remote diagnosis into `run_service.create`'s default ten-second planning envelope.
4. Create the persistent Run through `run_service.create`. Store the returned exact validated Plan and version. Human approval endpoint checks operator session, run ownership, CSRF, displayed Plan digest and manifest digest, then calls public `run_service.decide`. Persist explicit human events before acknowledging; partial event-write failures block admission.
5. Admit with `AdmissionCommand` after rereading the approved Run. Authorization is a separate authenticated click and public `gateway.authorize(ActionCommand(...), principal)`. Same operator may make both decisions; independence means separate exact decisions, not a claim of two-person separation.
6. The private service verifies its server-held AIG capability through `CapabilityVerifier`; it is not a browser login credential. Use one service subject for this single-operator MVP and immutable human-to-service correlation. An authorization click cannot come from model output or page load.
7. Execute through public gateway with CAS versions and stable command idempotency keys stored before dispatch. Never resend an uncertain execute to obtain a greener result. Read status first. Known rejected-before-claim commands may be corrected only without changing the approved content.

## 4. Queue transaction and receipt

Separate private AIG ledger and consumer SQLite database on local persistent disk. Consumer connections use foreign keys, WAL, `synchronous=FULL`, bounded busy timeout (initial target 250 ms) and `BEGIN IMMEDIATE`. Verify PRAGMA results and storage behavior, not only requested settings. No remote DB, Redis or distributed queue in v1.

Conceptual consumer constraints:

```text
store_identity(singleton PK, complete_binding_json, policy_revision, schema_digest)
trial_manifests(trial_id PK, manifest_digest UNIQUE, manifest_bytes, immutable)
governance_links(trial_id UNIQUE, run_id UNIQUE, action_id UNIQUE, plan_digest, human_events)
enqueue_effects(effect_key PK, payload_digest, trial_id UNIQUE, receipt_id UNIQUE, job_id UNIQUE)
enqueue_receipts(receipt_id PK, canonical_body, body_digest)
jobs(job_id PK, trial_id UNIQUE, effect_key UNIQUE, manifest_digest, receipt_id UNIQUE,
     state, version, worker_epoch, heartbeat_at, terminal_verdict)
job_events(job_id, seq, event, PRIMARY KEY(job_id,seq))
```

At executor entry capture `spec.payload_digest()` and the **AIG-provided UUIDv4 effect key**; never derive or replace it. Command idempotency keys, HTTP draft keys, trial ID and effect key serve different purposes.

One transaction verifies preprovisioned store identity and immutable manifest, then looks up the effect key. Same key/full payload and consistent job/receipt returns the original receipt. Same key/different payload returns `PAYLOAD_CONFLICT` without overwriting. A second effect key targeting the same trial is also rejected; it cannot create a second job. Any inconsistent existing rows produce Unknown/quarantine, not repair-on-write.

For a new effect insert exactly one `HELD` job, effect row, full receipt body and event in the **same transaction**. Check cancellation/deadline before COMMIT. After COMMIT reopen read-only and verify the committed rows and exact correlations within the adapter deadline. Only then return `ToolOutcome(Outcome.SUCCESS, effect_key, scope, target, payload_digest, receipt_uuid)`. No process creation, Docker RPC, inference or worker wait occurs in this executor.

Receipt body: schema `faultline-enqueue-receipt-v1`, UUID receipt/job/trial/effect IDs, AIG payload digest, manifest digest, complete binding identity, policy revision, admitted UTC time and state `HELD`. Later worker results do not rewrite this historical queue receipt. Its UUID is the AIG `receipt_reference`; product APIs resolve the full body through an allowlisted ID.

Recognized proven no-effect reasons are `INPUT_REJECTED`, `PAYLOAD_CONFLICT`, `STORE_IDENTITY_MISMATCH`. Exceptions, uncertain commit/readback, deadline expiry or late acknowledgment return `Outcome.UNKNOWN_OUTCOME`; do not invent no-effect reason strings. AIG validates outcome correlation and owns Action finish. Consumer durability is not an atomic transaction with AIG finish.

## 5. Worker claim, lifecycle and recovery

```text
HELD -> READY -> CLAIMED -> PREPARING -> BASELINE_RUNNING -> CANDIDATE_RUNNING
     -> VERIFYING -> CLEANING -> COMPLETED
Any owned stage -> CLEANING -> FAILED | INCONCLUSIVE
Any ownership/lifecycle ambiguity -> QUARANTINED -> read-only inspection + deliberate cleanup
```

`COMPLETED` carries deterministic recovery verdict PASS or FAIL, containment result and cleanup result separately. Lifecycle state is not a green verdict. `NOT RUN` is used for absent measurements; missing evidence yields INCONCLUSIVE. A known policy/security violation yields FAIL with explicit incomplete-evidence flags even if cleanup also fails.

Single worker claims `READY` using one SQLite CAS transaction: expected state/version, new persisted epoch/owner, attempt count exactly one. Persist container/network names and intended operation **before** each Docker create/start request. Names are trusted UUID-derived identities, not model text. Labels bind deployment scope/job/variant/manifest/epoch. Retain IDs and event sequence after successful calls.

The worker heartbeat is for detection only (design: every 2 s; stale after 10 s). It does not grant takeover. A worker/control-plane restart must prove the predecessor stopped before new work; `predecessor_stopped=True` is an operator attestation, not a kill command. For stale active work, stop new trials, quarantine the job and inspect known IDs/names/labels. Never clear the epoch and dispatch baseline/candidate again. Docker create/start acknowledgment loss is ambiguous even if the DB lacks a returned ID.

Trusted worker alone manages Docker; public API has no socket access. Use fixed image/command/configuration, and the immutable source-volume initialization described in the fixture specification. Record initializer/container/network/volume identities before dispatch and verify their exact removal. Baseline and candidate run sequentially under the same caps; no concurrent trial contaminates measurements.

Nominal total trial deadline 120 s, hard overall bound 180 s including a reserved 20 s cleanup envelope. Record per-stage deadlines from the monotonic job clock, with UTC correlation. Start no further stage when its minimum budget plus cleanup reserve cannot fit. At deadline/cancel: persist intent, stop owned containers with a 2 s grace then kill, inspect, remove exact resources, record residuals. A cancel request is authenticated and idempotent; it never sets “rolled back” or converts missing results to PASS. Ambiguous stop/removal becomes quarantine and blocks new trials.

## 6. Ownership and acceptance

Runner owns lifecycle observations; trusted probe/mock own raw measurements; evaluator owns verdict; artifact writer owns immutable hash-addressed storage and registration. Candidate stdout, a model statement or candidate-written JSON cannot create authoritative evidence. Worker lacks permission to overwrite the approved manifest. The UI reads separate AIG admission / trial / containment / cleanup states.

Before live use, test: wrong tool/target/binding/scope/profile, missing/stale consent and authorization; schema extra fields/types; same/different-key duplicates; concurrent inserts; lock timeout; crash before/after COMMIT; lost adapter acknowledgment; AIG finish failure; held-job release restart; worker crash before/after create/start; stale heartbeat; cancellation; missing/late receipts; no second enqueue or sandbox effect. Assert reopened DB rows and external lifecycle counts, not printed messages. All are **NOT RUN** in Phase 0.

Sources: [installed API decision](../AIG_VERSION_DECISION.md), [SQLite transaction semantics](https://sqlite.org/lang_transaction.html), [SQLite synchronous/WAL durability](https://sqlite.org/pragma.html#pragma_synchronous). Disk/VFS honesty, VM compromise and power-loss durability remain limits of the actual deployment.
