# Vultr readiness, delivery and evidence runbook

Date: 2026-10-19. **Design only. No cloud resources, inference requests or deployment have been performed.** This runbook is not spending authorization. Distinguish this completed preparation (“Phase 0 design”) from future **P0 infrastructure**.

## Minimal topology

One authorized Vultr Linux VM with supported Python 3.13 and Docker/cgroup controls. Planning capacity target: 4 vCPU / 8 GiB RAM / 40 GiB disk; actual SKU, region, architecture, availability and price remain UNVERIFIED. Measure contention before accepting replay results. No managed Kubernetes, database, object storage or per-task VM provisioning in v1.

Caddy or nginx serves HTTPS and Vite static assets, proxies the FastAPI control plane, and exposes only public result reads plus authenticated product endpoints. API holds the AIG single-owner context and inference client, but has no Docker socket/group. An independently supervised trusted worker/runner owns bounded Docker operations. Local persistent disk stores a private AIG gate, separate consumer SQLite WAL DB and immutable artifacts outside the web root. Serve downloads only by registered artifact ID.

Single private operator session supports real approval/authorization; public visitors inspect a published sanitized result and download its evidence without credentials. Do not distribute the AIG capability to browsers or expose the bundled runtime HTTP/UI as a public execution interface. When a live interactive mutation interface cannot pass authentication/CSRF/ownership checks, ship protected operator controls and public read-only results.

## Preconditions before provisioning

Recheck O-01–O-07 in [requirements](REQUIREMENTS_TRACEABILITY.md), current permitted implementation window, official event rules, user authorization and live Vultr prices. General lablab.ai guidance generally permits existing open-source infrastructure dependencies such as pinned AIG, subject to event-specific rules; the current reuse risk is LOW — pending event-specific confirmation. Organizer clarification is optional additional assurance and does not gate bounded infrastructure preparation. Confirm account access/credit eligibility, billing exposure, region/SKU, domain/DNS control, operator identity, approved duration and shutdown owner before provisioning. No enrollment, login, terms acceptance or credentials changes are implied by this document.

Proposed **approval ceilings**, not price quotes: USD 30 VM/storage/network, USD 10 inference, USD 10 contingency, USD 50 total until a specified shutdown time. The user must approve actual resource/call scope and amounts. Credits are not proof of zero charges or a confirmed entitlement. Quote actual hourly/monthly/resource/subscription charges before spend; reject a plan that exceeds the approved ceiling. If provider spend enforcement is not hard, state this explicitly and use conservative local request caps plus operator monitoring; do not call a budget alert a provider-enforced hard stop.

Store infrastructure and inference credentials separately in OS-protected files/service credentials, never repository `.env`, shell history, screenshots or exports. Use least-privilege/account capabilities actually supported; do not invent token scopes. Sandbox gets neither. Record only key-present/configured booleans and safe fingerprints where justified, never raw tokens.

## Deployment order (future authorized P0)

1. Produce a reviewable exact VM/region/cost/expiry proposal. Provision only after the required explicit approval. Record VM ID and scope privately; redact management details from public exports.
2. Apply firewall: HTTPS public, management SSH only from approved source, no Docker/runner ports. OS update and dedicated service identities. Verify actual inbound rules and TLS certificate; record build/runtime/kernel/cgroup facts.
3. In Faultline's own clean Python 3.13 environment, create `pyproject.toml`/`uv.lock` with the full AIG pin, install locked dependencies and verify metadata/direct URL/site-packages/RECORD. No adjacent source import. Keep separate preprovisioned stable gate/queue/binding identity.
4. Install API/worker service supervision with explicit stop/start and predecessor verification. Reject overlapping API owners. Protect DBs, inference credential, capability and artifacts with minimal file permissions. Test SQLite PRAGMAs/storage and restart persistence.
5. Qualify Docker privilege/resource/network profile. Run only the approved harmless sandbox check, inspect resulting settings/counters, record container/image/network identities, then remove exact owned resources and verify absence. Rootless mode is accepted only with actual working cgroups. No global prune.
6. Under separately approved inference allowance, discover available model(s), select one and make the minimum genuine connectivity request. No provider fallback, tool dispatch or repair experiment in P0. Record redacted request/response model, provider/base URL, response/request IDs when supplied, client correlation, monotonic timing, UTC, token usage or explicitly unavailable usage.
7. Expose a minimal truthful public health/readiness route and HTTPS page. Validate from a real external browser. `inference_configured=true` is not `inference_verified=true`. Restrict mutations until all relevant gates pass.
8. Review evidence/cost inventory, note unresolved failures and stop at P0. P1 fixture implementation needs its own instruction.

## Inference contract and unresolved API facts

The [event](https://lablab.ai/ai-hackathons/vultr-hackathon) specifies base URL `https://api.vultrinference.com/v1`; the [Vultr Python guide](https://docs.vultr.com/how-to-use-vultr-serverless-inference-in-python) documents chat completions and OpenAI-compatible requests. This documentation supports the protocol direction, not account access or actual model quality. The Python guide's model-list example uses `/v1/chat/models`; [newer Vultr documentation](https://docs.vultr.com/how-to-rank-documents-with-vultronretriever-on-vultr-serverless-inference) shows `/v1/models`. Confirm the currently supported route in authorized P0; do not assume the difference is harmless.

Start with plain chat completion output parsed by a closed local schema; no function-calling, RAG, external tools or provider-enforced JSON feature is required. Confirm selected model, context/output limits, JSON/patch reliability, returned model identity, usage field semantics, subscription pricing and 429/timeout behavior. P0 live model and fallback detection remain NOT RUN.

Future planning cap: at most one accepted proposal per draft, at most two explicitly initiated draft calls per operator per ten minutes, 2,048 maximum output tokens/call, 8 KiB bounded proposal, no automatic provider retries. Initial HTTP targets: connect <=5 s, total <=30 s, bounded response bytes; record timeout as failed/unverified planning and charge ambiguity honestly. A provider call is not retried because a local request timed out. Requested/returned model disagreement blocks candidate admission pending review; a documented alias requires explicit trusted mapping, not silent acceptance. A missing provider request ID is reported as unavailable with local correlation, not fabricated.

## Evidence Passport contract

JSON/ZIP v1 includes:

- `schema`, trial/manifest/input identities; fixture revision/tree/base and candidate provenance; scenario vector, seed, workload, probe/test/evaluator version/digests and thresholds.
- Exact Plan digest/Run/version, product human-approval and authorization event references, AIG Action/effect/payload/receipt, queue release observation, worker epoch and event sequence. No tokens/private DB exports.
- Genuine model provider/requested+returned model, safe correlation, timings/usage/response digest; exact reviewed patch/tree.
- Per-variant container/network IDs and sanitized configuration, lifecycle/timeout/resource observations; raw trusted quote/health/upstream data with ownership and counts.
- Independent recovery, containment and cleanup decisions with predicate/reason provenance; missing/NOT RUN fields and limitations remain visible.
- Artifact inventory: opaque ID, trial/variant, kind, safe relative path, byte count and SHA-256; public projection version/redaction declaration. Secrets and sensitive private audit remain outside the public bundle.

Canonical package manifest hashes actual exported bytes. Do not hash its own final ZIP into itself: publish the completed ZIP hash separately. Original private bytes and redacted public bytes have distinct hashes; disclose redaction. Use exclusive/no-follow file writes, atomic finalization and DB registration, reject symlinks/path traversal/duplicate ZIP names/oversized entries. Never trust sandbox filenames as export paths.

The future offline verifier must recompute each file digest, manifest identity, patch/tree/scenario correspondence, trial/variant relationships and deterministic metrics/predicates, detecting missing/swapped/tampered artifacts. Include the frozen evaluator protocol/source for reviewer reproducibility. The verifier validates the evidence's internal consistency; it does not attest a non-malicious host. No signing claim in v1. Before publication re-scan the actual exported bytes for tokens, personal data and executable web content.

## Shutdown and recovery

Disable new planning/admission; hold unclaimed work. Wait for safe owned work completion or authenticated cancel; preserve Unknown/quarantine. Inventory scope-labelled IDs from the durable ledger; inspect, stop/remove only those exact trial containers, initializers, networks, source volumes and workspaces and verify absence. Flush/checkpoint/back up SQLite through supported mechanisms including WAL consistency, finalize evidence/hash inventory, stop API/worker cleanly and verify predecessor absence. Never clear a ledger to make recovery green.

Delete the approved VM/storage only with explicit resource-specific authorization and after retaining required evidence. Guest shutdown is not assumed to stop billing. Record actual provider deletion/remaining inventory/cost status; unresolved resources remain reported. No self-deletion at an unreviewed TTL or destructive global cleanup.

## Critical path and time budgets

Budgets are focused engineering estimates for one developer: **46 h + 10 h contingency**, within 127 elapsed event hours only if account/API prerequisites are ready. Not an award or completion guarantee. Dates are NZDT planning targets; dependencies and separate authorization control progression.

| Phase / target | Scope and dependencies | Deliverables and acceptance evidence | Failure / cut rule | Budget |
|---|---|---|---|---|
| P0 / Nov 4 | Permitted window; operation-specific budget approval; VM+inference+HTTPS | Genuine model response, installed own-env AIG pin, harmless sandbox+cleanup, external HTTPS | Missing auth/model/resource controls or billing approval -> BLOCKED; unresolved reuse confirmation alone does not block bounded infrastructure preparation; no UI polish | 6 h |
| P1 / Nov 4–5 | P0 passes; baseline fixture only | Frozen image/vector/harness; 200-sample degraded baseline; qualification reference and raw outcomes | Failure not reproducible -> revise fixture/version before P2; cut optional incidents | 7 h |
| P2 / Nov 5–6 | Qualified fixture + exact public AIG API | Real proposal/frozen diff; human gates; atomic HELD enqueue/release; candidate replay and receipt/persistence tests | Unknown/duplicate/approval gap -> stop; cut all repair revision loops | 12 h |
| P3 / Nov 6–7 | Working bounded trial | CT-01–10, crash/ACK matrix, actual lifecycle counts, honest FAIL/INCONCLUSIVE and teardown | Any leak/forbidden effect blocks live demo; cut extra scenario products | 8 h |
| P4 / Nov 7 | P2/P3 evidence | Public result UI, JSON/ZIP verifier, tamper tests, external browser/anonymous mutation denial, restart smoke | Unverifiable result stays unproven; cut SSE/animations/PDF/signing | 7 h |
| P5 / Nov 8 | Stable complete workflow | Fresh full smoke, repeatability/cleanup, README/license/notices, video/deck/cover, checked links/forms | No fake green substitution; retain failed runs; submit by internal target | 6 h |

A slim browser view starts in P0/P1 for observability; P4 is polish and evidence integration, not the first time anyone sees the workflow. Keep operational buffer for quota/model outages and final recording. If P2 cannot complete by end Nov 6, cut presentation extras immediately; governance/isolation/evidence are release gates and cannot be traded away.
