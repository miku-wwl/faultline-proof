# Hackathon Agent Instructions — Reuse Agentic Intent Gate

## Purpose

This repository is a **Hackathon application that consumes an existing Python Agent Runtime**. Build the competition-specific product, **not another agent execution framework**.

**Shared runtime:** [Agentic Intent Gate](https://github.com/miku-wwl/agentic-intent-gate)<br>
**Python distribution:** `agentic-intent-gate`<br>
**Public integration module:** `agentic_intent_gate.runtime`<br>
**Qualified release:** `v0.2.0` (verified annotated Git tag; Python 3.13; MIT)<br>
**Pinned release commit:** `7261fdd2f47d2b15fabe8faac527eeee37338eb1`

The annotated tag `v0.2.0` peels to the pinned commit above. This is a **Git release, not a PyPI publication**. Use the immutable full commit SHA, **not** a moving `main` branch. When upgrading in the future, verify the tag, peeled commit, installed version, and lockfile. Never embed private Git credentials or external-service secrets in URLs, code, screenshots, or logs.

**Template use:** Copy this document into a **new consumer repository** as its root `AGENTS.md`. Add the competition's own scope, security rules, environment constraints, and human-approval requirements. If that repository already has `AGENTS.md`, **merge** the instructions instead of overwriting its product-specific rules. Do not copy the core repository's developer-only root `AGENTS.md` into a consumer project.

## Dependency Setup

Declare this exact dependency in the consumer's existing `pyproject.toml` and update its lockfile:

```toml
[project]
dependencies = [
  "agentic-intent-gate @ git+https://github.com/miku-wwl/agentic-intent-gate.git@7261fdd2f47d2b15fabe8faac527eeee37338eb1",
]
```

**Merge the dependency entry**; do not replace an existing `[project]` section or other dependencies blindly. Verify the installed distribution reports `agentic-intent-gate==0.2.0`, resolves to the pinned source commit, and is imported from the installed environment, **not an adjacent source checkout**. Use the [v0.2.0 consumer handoff](https://github.com/miku-wwl/agentic-intent-gate/blob/main/docs/V0.2.0-CONSUMER-HANDOFF.md) and [adapter guide](https://github.com/miku-wwl/agentic-intent-gate/blob/v0.2.0/docs/ADAPTER_GUIDE.md) as the detailed integration references.

## Reuse the Core

Within its supported scope, Agentic Intent Gate already provides:

- Strict structured Plan validation and trusted, bounded tool schemas.
- Persistent Runs and exact Plan-to-Approval binding.
- Independent Action execution Authorization, separate from Plan Approval.
- Explicit trusted single-tool `ToolExecutor` registration.
- Single-step `SIDE_EFFECT` Action lifecycle.
- SQLite-backed durable Action state, claim, audit events and receipt references.
- CAS/concurrency controls, stable effect keys, binding identity and idempotent command handling.
- Fail-closed recovery and terminal ambiguous/`Unknown` outcomes (no blind retry).
- Trusted configurable adapter execution budgets: default **5 seconds**, explicit maximum **15 seconds**.

**Do not copy, fork, reimplement, monkeypatch, or bypass these core mechanisms in the consumer.** Use the published public API and a fixed dependency revision.

## Public Integration Entry Point

Inspect the **installed v0.2.0 API** and the core repository's `examples/consumer/app.py` before implementing integration. Supported imports include:

```python
from agentic_intent_gate.runtime import (
    ToolBinding,
    ToolCapability,
    ExecutableRegistry,
    CapabilityVerifier,
    BoundCapabilityAuthorization,
    execution_budget_binding,
    open_runtime,
)
```

Check the actual constructor/function signatures; do not invent methods. Register trusted executors at startup with exact tool/version/target/adapter identity, reviewed binding revision, canonical execution scope, strict argument schema and appropriate independent authorization. Model output and untrusted HTTP input cannot register code or select trusted identities.

### Trusted Execution Budget (v0.2.0)

- `open_runtime(..., execution_timeout_seconds=5)` is the **backward-compatible default**. Finite built-in `int`/`float` values in `(0, 15]` are supported. Booleans, invalid types, NaN, infinity, non-positive values and values over 15 are rejected.
- For values **above 5**, trusted host code must explicitly opt in, use a **fresh reviewed base `ToolBinding` revision**, and apply `execution_budget_binding(base_binding, 15)` to produce a canonical binding revision ending in `.exec-15s`. The complete revision must fit the 64-character limit.
- Pass `execution_timeout_seconds=15` to `open_runtime` **only after the complete reviewed binding, capability, registry, verifier, policy and consumer effect/receipt identity are consistently configured**. Do not let model output, tool arguments, browser parameters, or API clients choose or increase this value.
- Keep the extended profile's binding revision, scope and persisted consumer configuration **stable across restarts**. Use a fresh UUIDv4 scope and **separate private gate/ledger/receipt-store identity** for a new extended profile.
- **Do not silently elevate old Actions or grants.** Never migrate, relabel, replay, or reuse legacy Approval, Authorization, effect keys or receipt identities under a longer budget. Create a new Plan/Run, obtain fresh human Approval, admit a new Action and obtain separate Authorization. Existing default-profile Actions retain their original identities; previously Failed/Unknown terminal Actions must not be reset or replayed.
- Extended Actions use `action-compiler-v3` / `action-spec-v3` and bind the reviewed budget profile into their identity. Old v1/v2 Actions cannot gain a longer budget merely by changing host configuration or using a similar binding name. Keep prior ledgers available for historical audit; v0.1.0 software cannot interpret v3 extended Actions.
- The configured adapter deadline starts **after durable Gateway claim**. The Gateway's synchronous claim and finish work are outside the adapter timer. A caller-supplied validated **monotonic** deadline may only **shorten**, never extend, this budget. Late outcomes, cancellation, lost acknowledgment and uncertain writes can still become `Unknown`.
- Provider requests, independent effect verification and adapter-side durable receipt persistence must fit within the adapter budget. External effects cannot necessarily be cancelled after dispatch. Avoid detached background execution, automatic retries, and recovery replay; **15 seconds is not a guaranteed completion time or exactly-once remote-effect guarantee**.
- The bundled Runtime Action HTTP routes retain a **10-second parent deadline**. If the consumer needs a full 15-second adapter allowance, use a supported public Gateway invocation within an appropriately budgeted **consumer-owned request envelope**; do not use private Runtime internals or assume the bundled HTTP endpoint grants 15 seconds.
- Consumer-specific constraints, including Sandbox-only execution, allowed targets, spend limits, HTTP timeouts, durable dispatch fencing and payment-provider policies, belong **in the consumer application**, not in the shared Runtime.

**Default rule:** Unless a reviewed use case needs an extended budget, omit the new argument and retain **5 seconds**.

## Competition-Specific Responsibilities

Implement **only** the product-specific requirements:

1. Product concept, competition integrations, frontend and demo experience.
2. Trusted consumer tools, bounded argument schemas, concrete executors and receipt stores.
3. External service/API/MCP clients, where genuinely needed.
4. Consumer authentication, authorization, credentials and environment controls.
5. A suitable consumer `ModelProvider` when model-driven Plan generation is required.
6. Product tests, evaluation, deployment, documentation and submission.

**Demo boundaries:** The core's bundled local LLM prompt is tailored to `service-demo/service_id`, and its UI Action-admission controls remain Demo-specific. A non-Demo consumer must provide suitable planning and its own UI or use supported API admission paths; the bundled Demo UI does **not** automatically support arbitrary tools. The reference consumer's scripted approval is test/example consent, not proof of authenticated human approval.

## Supported Scope and Non-Goals

v0.2.0 supports **one explicitly registered trusted `SIDE_EFFECT` tool per Runtime composition and single-step execution**. It is **not** a general-purpose multi-agent engine. Do not assume general `READ_ONLY` tool execution, multi-tool/multi-step workflow orchestration, dynamic plugin discovery, arbitrary MCP execution, production multi-user authentication, distributed HA, malicious-Python isolation, or guaranteed exactly-once remote side effects.

If the competition requires unsupported functionality, identify the gap before building. Prefer a thin product-owned layer where safe. Request a separately reviewed core extension only when unavoidable; never silently bypass the core's safety gates.

## Mandatory Safety Boundaries

- Model output proposes a Plan; it **never** chooses trusted credentials, executors, scopes, execution budgets or grant decisions.
- Verify exact tool identity, schema, target, binding revision, execution scope and trusted profile before compilation and execution.
- **Human Approval and execution Authorization are separate gates**. Approval alone never dispatches an effect; do not fabricate or inherit consent from earlier Actions.
- Never substitute a different Plan's Approval, skip durable claiming, or weaken owner fencing and authorization checks.
- Treat ambiguous post-dispatch effects as `Unknown`; **no automatic retry, unsafe reconciliation, duplicate POST or recovery replay**. Distinguish proven pre-dispatch no-effect failures from uncertain remote effects.
- Respect the provider's documented idempotency semantics; a provider request ID is **not** a universal exactly-once guarantee.
- Keep secrets, capability tokens, private Git credentials, personal data and private state outside source, docs, screenshots and CI logs.
- Do not initiate real money movements, financial API mutations or other irreversible third-party effects without fresh, explicit, operation-specific human authorization.

## Acceptance Criteria

An external consumer using the exact pinned, **installed** package, **without modifying core source**, must demonstrate:

**Validated Plan → Persistent Run → Exact Human Approval → Admission → Independent Authorization → Durable Action Claim → Consumer Executor → Verified Effect → Durable Receipt**

Tests should cover successful execution and persistence; unknown tool, wrong target/binding/scope, missing authorization, stale approval, duplicate/concurrent/conflicting effects, and ambiguous outcome. For extended profiles, additionally test default/15-second configuration, invalid budgets, wrong-profile denial, old-Action non-escalation, shortening caller deadlines, pre-dispatch expiry, lost acknowledgments, late receipts and process restart/recovery **without a second effect**. Verify actual durable state rather than only printed success. Synthetic planning is acceptable for offline tests; genuine external side effects need separate permission.

## Agent Work Protocol

Before changing code:

1. Read this `AGENTS.md`, other local instructions and actual competition requirements.
2. Verify the exact pinned dependency, installed public API, package version and lockfile.
3. Read the shared Runtime's `examples/consumer/app.py`, v0.2.0 handoff and adapter guide.
4. Propose the smallest **consumer-specific** implementation and targeted tests.
5. Flag missing capabilities rather than inventing public APIs or modifying the shared Runtime.

During development, preserve existing project state and security constraints. Keep changes scoped; use safe synthetic tests by default. **Do not commit, push, tag, release, deploy or run real external effects unless separately instructed.**

**Guiding rule: Build the Hackathon application; reuse the pinned Agentic Intent Gate Runtime.**

---

# Faultline Proof — Competition-Specific Instructions

> This section extends the upstream Agentic Intent Gate consumer instructions above. It applies specifically to the `faultline-proof` repository. If a proposed implementation conflicts with an upstream AIG invariant, **stop and report the conflict**; never weaken the invariant. Read the latest `docs/MASTER_DESIGN.md` for product details and `docs/AIG_VERSION_DECISION.md` for the dependency decision.

## Product Identity and Competition Goal

- **Product:** Faultline Proof — *Fix the incident. Prove the recovery. Contain the risk.*
- **Competition:** Vultr Agent Rush Hackathon, *Blast Radius Zero: Safe Agent Execution on Vultr*; confirm the latest official dates, implementation eligibility, technical rules and submission requirements before acting.
- **Outcome:** Demonstrate a real incident-response Agent that diagnoses a bounded outage, proposes a bounded fix using **Vultr Serverless Inference**, validates the original and repaired variants in isolated Vultr-hosted sandboxes, and produces a reproducible **Evidence Passport**.
- **Competitive differentiator:** Before/after **counterfactual incident replay**, measured SLO recovery, actual isolated execution, meaningful containment proof, human governance and reviewer-verifiable evidence. Not a generic chatbot, code-fixer, browser agent, unrestricted shell runner or another Agent Runtime.
- **Primary hero scenario:** `retry-storm-503`. The baseline must demonstrably fail under a fixed replay workload and the candidate must be evaluated under the **same conditions**. The mandatory negative scenario is `suspicious-log-injection` to exercise policy and instruction-boundary enforcement.
- **No production mutation:** Patches/configuration changes are confined to disposable trial environments. The product exports a reviewable candidate patch; it never silently deploys to production, pushes to external GitHub repositories or executes irreversible third-party changes.

## Authoritative References and Precedence

1. This complete root `AGENTS.md`, including the upstream AIG consumer rules.
2. Official Vultr Agent Rush rules and the latest official live dashboard; external facts in older documents are **not** an excuse to skip re-verification.
3. `docs/MASTER_DESIGN.md` for product implementation and scope, plus `docs/AIG_VERSION_DECISION.md` for the v0.2.0 pin.
4. The **installed** public AIG v0.2.0 API; the annotated `v0.2.0` tag, `examples/consumer/app.py`, the release handoff and the tagged adapter guide.
5. Actual code, local tests, cloud-side results and immutable evidence; never infer achieved behavior from design prose, mocked outputs or screenshots alone.

If sources differ, identify the exact mismatch in the phase report. The official contest rules control eligibility; the stronger proven safety invariant controls execution. Do not silently reinterpret either.

## AIG Integration Contract — Exactly One Governed Effect

- Keep `agentic-intent-gate==0.2.0` pinned to the full Git commit `7261fdd2f47d2b15fabe8faac527eeee37338eb1`. Never depend on moving `main`, fork the core, copy internal modules or assume undocumented API behavior.
- Register **one** host-defined trusted `SIDE_EFFECT` capability in each Runtime composition: `enqueue_incident_trial/1` (final exact public API identifiers and flat argument schema must be checked against the installed v0.2.0 API).
- The bounded manifest, policy version, scenario identity and input digest must be determined and verified by trusted code. The model may recommend a repair; it may **not** choose binding, scope, tool identity, credentials, executor, approval, trusted thresholds or execution budget.
- Enforce **Validated Plan → Persistent Run → Exact Human Approval → Action Admission → Independent Authorization → Durable Claim → Idempotent Queue Insertion → Correlated Receipt**.
- The consumer executor performs only a **short, durable, uniquely keyed enqueue** inside the AIG adapter deadline (prefer default 5 seconds). Atomic job insert + effect-key/payload binding + durable receipt must be verified with persistence, restart and concurrency tests. Returning an HTTP 200 or printing a success message alone is insufficient.
- The executor must **not** run the 30–180-second experiment, spawn detached sandbox work, or wait for a background result. A separate product-owned trusted worker consumes durable jobs after the enqueue receipt is committed.
- AIG `Succeeded` means **queue admission only**. A worker trial has independent states and may fail, time out or remain `INCONCLUSIVE`; no UI or report may equate the two.
- Preserve fail-closed behavior: ambiguous Action dispatch is `Unknown`; do not auto-reissue the Action. Worker lease expiry or ambiguous container lifecycle must not trigger blind redispatch; quarantine, perform read-only inspection, and require deliberate recovery decisions.
- AIG does **not** implement general multistep tools, malicious-code isolation or authenticated product users. Those are explicit **consumer responsibilities**. Do not claim otherwise.
- Do not upgrade AIG merely because a trial is longer than 15 seconds. Upgrade only following documented evidence of a material security or public-API blocker, independent qualification and the user's explicit approval.

## Trusted Worker and Sandbox Security

- The API/control plane, queue/ledger, trusted worker, sandbox runtime and model API client are separate trust boundaries. The untrusted sandbox must never contain cloud keys, AIG capability tokens, SSH agents, host home mounts or Docker socket mounts.
- Only the trusted runner can request container lifecycle operations; untrusted task content must never interpolate into host shell commands or runner/container configuration.
- Use a fixed scenario allowlist, bounded patch paths, restricted image digests, least privilege, read-only root filesystem where feasible, ephemeral writable workspace, no unnecessary network egress, and enforced CPU/RAM/PID/wall-clock/concurrency limits. Test the actual container configuration and resulting behavior.
- Control-plane authentication, actual human approval and separate authorization are necessary for any live mutation endpoint. A publicly readable demo UI must not expose an unauthenticated mutable execution interface.
- Treat repository files, incidents, log messages, stack traces, generated patches, model responses and browser data as **untrusted inputs**. Prevent prompt-injected diagnostic logs from changing policy, model tools, approved scope or verifier rules.
- A bounded failure, timeout, denied operation or quarantine may be a **successful containment demonstration**, but does **not** prove universal isolation. Never assert absolute sandbox safety or no possible escape.
- Clean up every created trial container, network and temporary workspace. Persist independently measured teardown evidence; report leaks or ambiguous cleanup as unresolved rather than hiding them.
- Do not expose provider credentials in HTTP responses, model prompts, screenshots, logs, source, frontend bundles or submitted artifacts.

## Vultr and Evidence Requirements

- The deployed backend/runner and its sandbox execution must run on Vultr infrastructure as required by the contest. All **deployed Agent LLM requests** must go through **Vultr Serverless Inference**; local deterministic mocks are allowed only for transparently labeled offline tests.
- Record real provider/model identification, request correlation, timing and bounded usage without persisting credentials or raw sensitive data. Detect and report silent model fallback when a requested model differs from the actual response.
- For the golden-path trial, baseline and candidate must share immutable fixture revision, image/build provenance, replay seed, traffic profile, probe duration and decision thresholds. Do not cherry-pick samples, secretly rerun until success, or let the model choose success criteria.
- A **deterministic, trusted evaluator** determines whether the candidate recovered the incident without regression. Model-generated explanations are annotations, never the source of PASS/FAIL truth.
- The **Evidence Passport** must preserve input/fixture identities, manifest hash, Plan/Approval/Authorization references, queue receipt, sandbox identifiers and lifecycle, baseline and candidate raw measurements, patch digest, containment outcome, cleanup status, evaluator version and decision provenance. Bind artifacts to the correct trial and digest.
- Distinguish **PASS**, **FAIL**, **INCONCLUSIVE** and **NOT RUN**. A test, cloud call, screenshot, deployment, isolation feature, or model invocation is *real* only after its execution has been verified. Never create fake metrics, receipts, release claims or attractive but misleading green badges.
- A judge must be able to inspect the real result from a publicly reachable UI without privileged access, while mutation and sensitive evidence remain protected.

## Implementation Priority and Scope Discipline

- Design for a **single polished incident workflow first**: real Vultr deployment → actual inference → explicit approval/authorization → durable enqueue → actual baseline sandbox failure → bounded candidate repair → same-scenario replay → objective verdict → containment demonstration → Evidence Passport → clean shutdown.
- The core MVP does not require Kubernetes, a multi-agent framework, unrestricted MCP tools, general-purpose project import, third-party production APIs, payment operations or arbitrary production deployment.
- Favor one reproducible, reliable public demo over a large number of shallow features or synthetic-only test counts. Avoid refactoring working systems or adding new abstractions without a measured need.
- Use Python 3.13 for the AIG consumer as required. Other stacks/components should follow `docs/MASTER_DESIGN.md` unless a documented, evidence-based architectural change is approved.
- Keep all execution manifests and validation schemas explicit, closed and versioned. Fail closed on malformed input, missing receipts, timeouts, inconsistent hashes, unknown worker states and verifier failures.

## Contest Schedule and Stage Boundaries

- **Before official kickoff:** only research, documentation, competitor/compliance review and other preparation explicitly allowed by the official rules. **Do not implement competition-specific core functionality ahead of the permitted window.** Confirm the latest organizer interpretation of reusable scaffolding and AIG dependency attribution.
- **P0:** Vultr infrastructure and actual Serverless Inference connectivity with observable provider evidence.
- **P1:** Executable baseline incident and bounded sandbox lifecycle.
- **P2:** Real Agent plan, AIG-approved durable enqueue and measured candidate recovery.
- **P3:** Prompt-injection/containment fault cases, worker crash recovery, cleanup and honest `Unknown`/`INCONCLUSIVE` paths.
- **P4:** Public demo UX, traceability, artifact integrity, security hardening and repeatability.
- **P5:** Submission freeze, complete smoke run, short demo recording, pitch deck, README, license and final links.
- These labels are planning targets, **not automatic authorization**. Do not self-advance phases or incur Vultr costs without user authorization. When official dates change, update the plan with verified sources.

## Codex Sol — Execution Protocol

- **Primary development environment:** VS Code with Codex. **Preferred model:** Codex Sol. Default effort **High**; use **Extra High** for AIG contract design, sandbox security, distributed-state/race debugging or safety-critical review when available.
- For each task, first read root `AGENTS.md`, relevant design/ADR, current Git status, the existing code and tests. Make a concise plan; do not restart the project or replace its architecture without evidence.
- Execute **only the authorized phase**. Implement the smallest working vertical slice; add targeted tests and collect actual execution evidence. Fix failures before claiming PASS. Report new blockers honestly.
- Maintain deterministic tests for malformed plans, absent consent, identity/scope mismatch, duplicate/concurrent enqueue, ambiguous commit, crash/restart, prompt injection, resource isolation, sandbox destruction, equal-condition replay and evidence integrity.
- Do not run commands that mutate unrelated local repos, unrelated Docker resources or Kubernetes clusters. Never modify the ambient kube-context or use destructive global cleanup commands.
- **No commit, push, tag, release, deployment, external side effect or billable cloud action without explicit user authorization.** A phase instruction to inspect or design is not blanket approval to mutate external systems.
- Every phase report must state: `PASS / PARTIAL / BLOCKED`; files changed; commands and tests genuinely run; real evidence paths/IDs; unresolved risks; security decisions; exact next phase; and recommended **Codex Sol effort**.
- Stop at the approved phase boundary. Request approval for broadened scope, real resource provisioning or critical changes to the AIG dependency; do not silently continue.

**Final governing principle:** Build an award-competitive **Faultline Proof** product. Reuse the **unchanged, pinned** AIG Runtime for bounded consent and durable queue admission; execute only authorized experiments in isolated Vultr-hosted environments; measure recovery objectively; and make every important claim auditable.
