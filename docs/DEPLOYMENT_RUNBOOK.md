# Vultr readiness, delivery and evidence runbook

Date: 2026-10-19. **Deployment procedure prepared; cloud resources, inference requests and deployment NOT RUN.** Project-local dependency and generic Docker qualification are now recorded in the [pre-hackathon report](PHASE_REPORTS/PRE_HACKATHON_READINESS_REPORT.md). This runbook is not spending authorization. Distinguish preparation from future **M1/P0 infrastructure**.

## Minimal topology

One Ubuntu 24.04 LTS amd64 Vultr VM, recommended `vhp-4c-8gb-amd` in Sydney (4 vCPU / 8,192 MB / 180 GB local disk); fallback `vc2-4c-8gb` in Melbourne. Public catalog prices/capacity were checked, not reserved; account access and actual host behavior remain UNVERIFIED. See the [resource/cost plan](VULTR_RESOURCE_AND_COST_PLAN.md) for exact quotes, fallback and budget. Measure contention before accepting replay results. No managed Kubernetes, database, object storage or per-task VM provisioning in v1.

Caddy serves HTTPS and Vite static assets, proxies the FastAPI control plane, and exposes only public result reads plus authenticated product endpoints. API holds the AIG single-owner context and inference client, but has no Docker socket/group. An independently supervised trusted worker/runner owns bounded Docker operations. Local persistent disk stores a private AIG gate, separate consumer SQLite WAL DB and immutable artifacts outside the web root. Serve downloads only by registered artifact ID.

Single private operator session supports real approval/authorization; public visitors inspect a published sanitized result and download its evidence without credentials. Do not distribute the AIG capability to browsers or expose the bundled runtime HTTP/UI as a public execution interface. When a live interactive mutation interface cannot pass authentication/CSRF/ownership checks, ship protected operator controls and public read-only results.

## Preconditions before provisioning

Recheck O-01–O-07 in [requirements](REQUIREMENTS_TRACEABILITY.md), current permitted implementation window, official event rules, user authorization and live Vultr prices. General lablab.ai guidance generally permits existing open-source infrastructure dependencies such as pinned AIG, subject to event-specific rules; the current reuse risk is LOW — pending event-specific confirmation. Organizer clarification is optional additional assurance and does not gate bounded infrastructure preparation. Confirm account access/credit eligibility, billing exposure, region/SKU, domain/DNS control, operator identity, approved duration and shutdown owner before provisioning. No enrollment, login, terms acceptance or credentials changes are implied by this document.

Proposed **approval ceilings**, not price quotes: USD 30 VM/storage/network, USD 10 inference, USD 10 contingency, USD 50 total until a specified shutdown time. The user must approve actual resource/call scope and amounts. Credits are not proof of zero charges or a confirmed entitlement. Quote actual hourly/monthly/resource/subscription charges before spend; reject a plan that exceeds the approved ceiling. If provider spend enforcement is not hard, state this explicitly and use conservative local request caps plus operator monitoring; do not call a budget alert a provider-enforced hard stop.

Store infrastructure and inference credentials separately in OS-protected files/service credentials, never repository `.env`, shell history, screenshots or exports. Use least-privilege/account capabilities actually supported; do not invent token scopes. Sandbox gets neither. Record only key-present/configured booleans and safe fingerprints where justified, never raw tokens.

## Deployment order (future authorized P0)

1. Produce a reviewable exact VM/region/cost/expiry proposal. Provision only after the required explicit approval. Record VM ID and scope privately; redact management details from public exports.
2. Apply firewall: HTTPS public, management SSH only from approved source, no Docker/runner ports. OS update and dedicated service identities. Verify actual inbound rules and TLS certificate; record build/runtime/kernel/cgroup facts.
3. Transfer the reviewed source snapshot including the prepared `pyproject.toml`/`uv.lock`. On the VM create its own Python 3.13 environment, run `uv sync --locked` and reverify metadata/direct URL/site-packages/RECORD. Windows `.venv` is not transferred. No adjacent source import. Provision separate private stable gate/queue/binding identity only when implementing the authorized consumer, never from model/browser input.
4. Install API/worker service supervision with explicit stop/start and predecessor verification. Reject overlapping API owners. Protect DBs, inference credential, capability and artifacts with minimal file permissions. Test SQLite PRAGMAs/storage and restart persistence.
5. Qualify Docker privilege/resource/network profile. Run only the approved harmless sandbox check, inspect resulting settings/counters, record container/image/network identities, then remove exact owned resources and verify absence. Rootless mode is accepted only with actual working cgroups. No global prune.
6. Under separately approved inference allowance, discover available model(s), select one and make the minimum genuine connectivity request. No provider fallback, tool dispatch or repair experiment in P0. Record redacted request/response model, provider/base URL, response/request IDs when supplied, client correlation, monotonic timing, UTC, token usage or explicitly unavailable usage.
7. Expose a minimal truthful public health/readiness route and HTTPS page. Validate from a real external browser. `inference_configured=true` is not `inference_verified=true`. Restrict mutations until all relevant gates pass.
8. Review evidence/cost inventory, note unresolved failures and stop at P0. P1 fixture implementation needs its own instruction.

## Inference contract and verified documentation

The [event](https://lablab.ai/ai-hackathons/vultr-hackathon) specifies base URL `https://api.vultrinference.com/v1`. This sprint actually retrieved the public `/v1/models` catalog without credentials; the [current reference](https://api.vultrinference.com/docs/reference/list-models) documents this route. It supersedes the older Python guide's `/v1/chat/models` assumption for preparation. The [resource plan](VULTR_RESOURCE_AND_COST_PLAN.md#inference-decision-and-protocol) records primary `qwen3.8-27b`, deliberate fallback `minimax-m3`, advertised features/prices/limits/errors, source conflicts and a nonexecuting generic connectivity request. Subscription access, model behavior and paid connectivity remain NOT RUN.

Start with plain chat completion output parsed by a closed local schema; no function-calling, RAG, external tools or provider-enforced JSON feature is required. Confirm selected model, context/output limits, JSON/patch reliability, returned model identity, usage field semantics, subscription pricing and 429/timeout behavior. P0 live model and fallback detection remain NOT RUN.

Future planning cap: at most one accepted proposal per draft, at most two explicitly initiated draft calls per operator per ten minutes, 2,048 maximum output tokens/call, 8 KiB bounded proposal, no automatic provider retries. Initial HTTP targets: connect <=5 s, total <=30 s, bounded response bytes; record timeout as failed/unverified planning and charge ambiguity honestly. A provider call is not retried because a local request timed out. Requested/returned model disagreement blocks candidate admission pending review; a documented alias requires explicit trusted mapping, not silent acceptance. A missing provider request ID is reported as unavailable with local correlation, not fabricated.

## Operator bootstrap: fresh VM to HTTPS (future authorized M1/P0)

All remote commands/configuration below are **NOT RUN**. They are a procedure for an approved fresh VM, not infrastructure code shipped before kickoff. Do not execute against an unrelated server. M1 here means repository P0; it does not include P1 incident implementation.

1. **Before create:** confirm the official window, [account checklist](VULTR_ACCOUNT_CHECKLIST.md#consolidated-user-actions), exact console price/credits/subscription charges, one approved VM/region, public hostname, SSH public key/source IP, spending ceiling and hosting/teardown owner. Record provider IDs privately. Use an existing owned subdomain; no domain purchase is assumed. Recheck public plan availability and quote before the one VM creation. This sprint authorized none of those mutations.
2. **Host access:** verify the SSH host fingerprint through the console; use a key-authenticated non-root sudo operator. Keep a second verified session open before restricting password/root login. Create separate non-login `faultline-api` and `faultline-worker` users. Only the worker may control Docker; the API user must not be in the Docker group. No extra SSH agent forwarding. Inspect actual `sshd -T` and inbound connectivity before closing the bootstrap session.
3. **Packages:** on the approved Ubuntu host apply security updates; install Git, CA certificates, curl and systemd tooling. Install Docker Engine through its [official Ubuntu repository procedure](https://docs.docker.com/engine/install/ubuntu/), pin the reviewed package versions, and record kernel/Engine/cgroup v2 facts. Install the same uv version qualified locally (0.11.16), verifying the official release checksum; obtain Python 3.13.9 through uv in the service's managed environment. Recheck patch security at kickoff before changing the Python patch pin and record any intentional lock/runtime change. Terraform is optional and is not used for this single-console-deployment plan.
4. **Source/environment:** install a reviewed allowlisted release snapshot under `/srv/faultline/releases/<reviewed-id>`; expose `/srv/faultline/current` only after verification. At present the sprint changes are uncommitted and not available by checking out the earlier remote SHA; do not claim otherwise. Transfer source/lock/scripts only, never Windows `.venv`, `.env`, `.local`, private state or SSH keys. Run the commands below as the appropriate service/build identity; retain exit results and lock hash. Install Node/npm for the future Vite build only when there is an actual frontend manifest/lock; no frontend or `npm ci` target exists now.

```bash
# Future approved VM only, from the reviewed release directory.
uv sync --locked --python 3.13.9
uv lock --check --offline
uv pip check --python .venv/bin/python
.venv/bin/python -I scripts/preflight/verify_aig.py --output .local/aig-vm.json
```

5. **State/identity:** create the path/permission specification below, outside the static web root. Use separate local-disk AIG and consumer databases with verified WAL/FULL/foreign-key settings. Provision a new canonical UUIDv4 deployment scope and private capability once, retain them on restart and record the complete default-budget binding identity. No app module or identity-provisioning command is invented in this preparation package.

| Path / service | Owner/access specification |
|---|---|
| `/var/lib/faultline/gate/` | API only; mode 0700; private AIG ledger, capability and stable identity |
| `/var/lib/faultline/consumer/` | API and trusted worker only; shared trusted group, mode 0770; consumer jobs/effects/receipt DB |
| `/var/lib/faultline/manifests/` | API writes immutable approved bytes; worker read-only; public web user denied |
| `/var/lib/faultline/artifacts/` | Trusted writer owns immutable bytes; API reads registered IDs; no Caddy file root access |
| `/var/lib/faultline/work/` | Worker-owned disposable trial workspace; no home/secret mount into sandbox |
| `/etc/faultline/credentials/` | Root-protected credential sources, service-specific systemd `LoadCredential`; never a repository `.env` |
| `/srv/faultline/current/apps/web/dist/` | Static built frontend only, Caddy read-only; no source/DB/credentials |

6. **Supervision:** one systemd API process (`uvicorn` single worker, `127.0.0.1:8000`), one independent worker process, and Caddy. Do not expose `runtime.http_app()` or its Demo UI. Units use dedicated users, explicit working directories, `UMask=0077`, bounded file/process limits and no inherited SSH/cloud-management credentials. Bind future entrypoints only after they exist in M1/later phases; this document provides no fake `faultline` module. Initial API/worker `Restart=no`: a failure blocks new work and requires inspection/predecessor termination proof before deliberate restart. Caddy uses its vendor unit. Later automatic restart requires actual crash/quarantine tests; never turn lease expiry into permission to start another trial.
7. **Docker qualification:** use a local Unix-socket context on the VM; record its name rather than changing the workstation context. Run the generic smoke against the pinned image below, inspect cgroup values and exact cleanup, then implement/test the future worker profile within its authorized phase. The local WSL test used a rootful daemon; a rootful dedicated trusted worker is an explicitly privileged boundary, not proof of cloud isolation. Rootless is acceptable only after actual cgroup delegation/control checks; no switch is inferred from this plan.

```bash
# Future approved VM; choose its actual local Unix-socket context.
docker pull alpine@sha256:85fe1e81d6758c208f3e1eed4338a1997e19d4be002d4dd32d3100c9a8c010a0
.venv/bin/python -I scripts/preflight/docker_smoke.py --context default --image alpine@sha256:85fe1e81d6758c208f3e1eed4338a1997e19d4be002d4dd32d3100c9a8c010a0 --output .local/docker-vm.json
```

8. **Firewall and sandbox networks:** provider firewall allows TCP 22 only from the approved operator source and public TCP 80/443. Host firewall agrees; no 8000, Docker 2375/2376, SQLite or runner RPC port is public. Docker documents [published-port bypass of ufw](https://docs.docker.com/engine/install/ubuntu/#firewall-limitations); keep all trial ports unpublished and qualify Docker forwarding/input policy explicitly. Production trial networks are internal and still need host/metadata/public IPv4/IPv6/DNS denial tests from [CT-06](THREAT_MODEL.md#required-attack-and-fault-experiments). No broad firewall recipe is claimed tested here. Default deny plus intended service/mock/probe traffic must be observed on the actual host before live trials.
9. **DNS/TLS:** the approved VM's stable-for-its-lifetime primary public IPv4 gets one `A` record for the owned hostname, TTL about 300 seconds during setup. No reserved-IP service is needed. Add no `AAAA` until IPv6/firewall behavior is verified. Install Caddy from its [official package instructions](https://caddyserver.com/docs/install#debian-ubuntu-raspbian) and let [automatic HTTPS](https://caddyserver.com/docs/automatic-https) obtain/renew a publicly trusted certificate once DNS and ports 80/443 work. Domain ownership, certificate issue and public reachability are NOT VERIFIED. Do not use an insecure certificate bypass as the public demo.

The following Caddyfile is a **documentation template**, using a reserved example hostname. It is not deployed. Keep writes closed until real authentication/ownership/CSRF tests pass; then remove the write block only in a reviewed authorized deployment. Caddy supports WebSockets automatically; choose bounded polling for v1. If SSE is later implemented, qualify buffering/timeouts against the [reverse-proxy reference](https://caddyserver.com/docs/caddyfile/directives/reverse_proxy) before claiming streaming works.

```caddyfile
proof.example.com {
    encode zstd gzip
    @private path /.env /AGENTS.md /pyproject.toml /uv.lock /docs/* /state/* /artifacts/*
    respond @private 404
    @writes method POST PUT PATCH DELETE
    respond @writes 403
    handle /api/* {
        reverse_proxy 127.0.0.1:8000
    }
    handle {
        root * /srv/faultline/current/apps/web/dist
        try_files {path} /index.html
        file_server
    }
}
```

10. **Inference:** only after subscription/call-specific approval, use the [generic procedure](VULTR_RESOURCE_AND_COST_PLAN.md#nonexecuting-connectivity-example) once. Record sanitized model, usage and timing; never put provider headers/credential values in journal logs. The public health route can report configured/verified as separate fields. It cannot imply the incident product exists.
11. **First public check:** validate Caddy's config before reload, verify bound ports/units and test from an actual independent public browser. Required observations: trusted certificate, truthful health/readiness, protected or disabled POST, denied private paths, no Docker/runner exposure and no secrets in HTML/JS/source maps/logs. No browser test occurred in this sprint.

```bash
# Future host checks; no app/unit is assumed present before implementation.
sudo caddy validate --config /etc/caddy/Caddyfile
sudo ss -lntup
sudo systemctl status caddy faultline-api faultline-worker --no-pager
curl --fail --connect-timeout 5 --max-time 15 https://proof.example.com/api/healthz
```

### Persistence, operations and rollback

Journal retention target: 64 MiB / two days for this deployment, with credential/diagnostic redaction and no full environment/request headers. Bound stage stdout/stderr and artifact sizes per the existing threat model. Use a 2 GiB aggregate artifact admission ceiling initially; when full, reject new trials rather than deleting historical/Unknown evidence. Confirm free disk/image-cache space before a build. Keep evidence needed for judges through the approved hosting period.

Use SQLite's supported backup API or a quiesced consistent backup; never copy only a live main DB and omit required WAL content. Test reopen/readback before calling persistence PASS. Source releases are immutable; rollback stops admissions/model calls, proves API/worker predecessor termination, preserves quarantined work, backs up DB/artifacts and switches to a reviewed compatible release. Never roll the AIG ledger/identity back, reuse old grants for new effects or downgrade an incompatible schema. If compatibility is not proven, remain offline/read-only.

At shutdown follow the exact scope/ID procedure below and the [cost plan](VULTR_RESOURCE_AND_COST_PLAN.md#naming-expiry-and-teardown). A watchdog can detect expiry/stop admission; VM destruction and unverified trial cleanup are not silently scheduled. Retain actual provider deletion and billing evidence once authorized. Runbook readiness is not deployed-host acceptance.

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
