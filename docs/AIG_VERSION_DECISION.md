# AIG version decision — retain v0.2.0

Date: 2026-10-19, Pacific/Auckland. Status: **DESIGN VERIFIED; consumer installation NOT RUN**.

## Decision and evidence

Retain the unchanged Git dependency:

```toml
"agentic-intent-gate @ git+https://github.com/miku-wwl/agentic-intent-gate.git@7261fdd2f47d2b15fabe8faac527eeee37338eb1"
```

Read-only `git ls-remote` returned annotated tag object `b193d38a4804725d44ca536a3bd9778679cc7b4c` and peeled commit `7261fdd2f47d2b15fabe8faac527eeee37338eb1`. The [GitHub tag record](https://api.github.com/repos/miku-wwl/agentic-intent-gate/git/tags/b193d38a4804725d44ca536a3bd9778679cc7b4c) identifies a commit object and a tagger date of 2026-10-13T10:10:57Z. It reports an **unsigned** tag. Verified tag identity here does not mean a verified cryptographic signature.

The release [package manifest](https://github.com/miku-wwl/agentic-intent-gate/blob/7261fdd2f47d2b15fabe8faac527eeee37338eb1/pyproject.toml) specifies version `0.2.0`, Python `>=3.13,<3.14`, MIT, and FastAPI/httpx/jsonschema/uvicorn dependencies. The [license](https://github.com/miku-wwl/agentic-intent-gate/blob/7261fdd2f47d2b15fabe8faac527eeee37338eb1/LICENSE) names Weilai Wang, 2026. This is a Git release; do not substitute a guessed PyPI artifact.

An **existing installed environment in another consumer** was inspected read-only with isolated Python (`-I` in the retained verification): `D:\workshop\oct\pactlens\.venv\Scripts\python.exe`, Python 3.13.14. Distribution metadata reports `0.2.0`; `direct_url.json` reports the full pinned Git commit; the import resolves to that environment's `Lib/site-packages/agentic_intent_gate/runtime.py`. All 57 hashed RECORD entries match; `uv pip check --python <that interpreter>` passes. No packages or files in that other consumer were changed.

This proves availability and signatures of an installed release for design inspection. It **does not** prove a Faultline dependency installation, lock resolution, integration, or cloud execution. Faultline currently has no `pyproject.toml`, `uv.lock`, `.venv`, application or tests. Create its dependency manifest/lock only in the authorized implementation window and reverify the installation there.

## References actually inspected

- [Tagged reference consumer](https://github.com/miku-wwl/agentic-intent-gate/blob/7261fdd2f47d2b15fabe8faac527eeee37338eb1/examples/consumer/app.py).
- [Tagged adapter guide](https://github.com/miku-wwl/agentic-intent-gate/blob/7261fdd2f47d2b15fabe8faac527eeee37338eb1/docs/ADAPTER_GUIDE.md).
- [Tagged handoff](https://github.com/miku-wwl/agentic-intent-gate/blob/7261fdd2f47d2b15fabe8faac527eeee37338eb1/docs/V0.2.0-CONSUMER-HANDOFF.md), plus the [post-release handoff at its last-changing commit](https://github.com/miku-wwl/agentic-intent-gate/blob/3305eb179914c27d89628bc4a4e7e18e1893b5f9/docs/V0.2.0-CONSUMER-HANDOFF.md). The latter records the final release SHA; the tagged document cannot embed its own commit SHA.
- Installed public exports and signatures. Retained results: [inspection evidence](PHASE_REPORTS/evidence/P0_DESIGN_INSPECTION.md).

## Verified public composition

Imports come exclusively from `agentic_intent_gate.runtime`:

```text
ToolBinding(tool_name, tool_version, adapter_id, binding_revision, target, execution_scope)
ToolCapability(binding, description, input_schema, target_argument=None, semantic_rule=None)
ExecutableRegistry(executor=None, *, binding=None)
CapabilityVerifier(token=None, *, subject_id=None, binding=None, operations=())
BoundCapabilityAuthorization(verifier, *, policy_revision)
open_runtime(*, gate_path, provider, capability, registry, verifier, policy,
             predecessor_stopped=False, execution_timeout_seconds=5)
ToolExecutor.execute(self, spec, effect_key, context) -> ToolOutcome  [async]
```

Supported commands include `AdmissionCommand(run_id, expected_run_version, subject_id, idempotency_key)` and `ActionCommand(action_id, expected_action_version, idempotency_key)`. Public gateway methods include `admit`, `authorize`, async `execute(..., deadline=None)`, `get(action_id, principal)` and `list_for_run(run_id, principal)`. `run_service.create(Intent(...))`, `get` and `decide(ApprovalDecisionRequest(...))` support persistent planning/approval. Use versions returned by the runtime; do not copy the example's numeric versions into browser logic.

The closed argument-schema subset has 1–16 required bounded scalar fields, no nested values, arrays, optional fields, `enum` or `const`. Use bounded strings with anchored trusted patterns and deterministic semantic validation for allowlists. Identity scope must be canonical UUIDv4. The executor receives no Action ID or human token: link Action/Run/trial in consumer-owned governance records, not invented executor arguments.

## Why no upgrade

The one governed effect is durable queue admission. Its receipt transaction fits the default five-second adapter budget by design; experiments run separately. There is no demonstrated v0.2.0 public-API blocker. Keep the default; do not use the 15-second profile. The public gateway can read final Action state to release held jobs without core DB access or Unknown reconciliation.

Keep application auth, reviewed patch/manifests, queue atomicity, worker fencing, sandbox isolation, measurement and artifact integrity in Faultline. Do not expose `runtime.http_app()` as the public product: bundled UI/planning assumptions are Demo-specific and are not human authentication.

A reproducible security/API blocker would require a separate proposal and explicit approval. Longer trials, missing user auth or worker orchestration are not reasons to upgrade or copy core mechanisms.
