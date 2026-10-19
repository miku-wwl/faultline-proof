# Pre-hackathon readiness sprint report

Date: 2026-10-19, Pacific/Auckland. Scope: authorized local/research preparation only. Baseline HEAD: `ad5552bb012bc2c6db1ca508679816c9155863f4`. **PREP_STATUS=PASS** means the permitted preparation checklist is complete and remaining external user actions are explicitly identified. It does not mean the cloud/product works or that eligibility is guaranteed.

```text
PREP_STATUS=PASS
PYTHON_ENV_STATUS=PASS_LOCAL_WINDOWS
AIG_DEPENDENCY_STATUS=PASS_INSTALLED_PIN_0.2.0
DOCKER_PREFLIGHT_STATUS=PASS_LOCAL_GENERIC_ONLY
VULTR_ACCOUNT_STATUS=USER_ACTION_REQUIRED
VULTR_CREDITS_STATUS=PENDING_COUPON_PERSONAL_BALANCE_UNVERIFIED
VULTR_COMPUTE_PLAN_STATUS=PASS_PLAN_ONLY
VULTR_INFERENCE_PLAN_STATUS=PASS_PLAN_ONLY_LIVE_AUTH_NOT_RUN
HTTPS_DEPLOYMENT_PLAN_STATUS=PASS_PLAN_ONLY_DEPLOYMENT_NOT_RUN
COMPETITION_RULES_STATUS=CHECKED_PERSONAL_ELIGIBILITY_UNVERIFIED
M1_START_READINESS=CONDITIONAL_ON_WINDOW_USER_ACTIONS_AND_SPECIFIC_AUTHORIZATION
```

## A. Actual work and workstream results

| Workstream | Result | Evidence / practical limit |
|---|---|---|
| A — Local environment | PASS | Python 3.13.9, uv 0.11.16, Git 2.49.0.windows.1, Docker/Engine 29.8.0, Compose 5.5.1, Node 26.5.0, npm 12.0.1, PowerShell 7.6.7, OpenSSH 9.5p2. Terraform 1.14.0 is present/optional; no upgrade needed for the chosen console provisioning plan. [Inventory](evidence/PRE_HACKATHON_ENVIRONMENT.json) |
| B — AIG | PASS, installed dependency only | Own `.venv`, `0.2.0`, exact HTTPS source/pin, seven public exports/signatures, default 5 seconds, 57 RECORD hashes, lock/install/dependency checks. No Action or product adapter. [AIG](evidence/PRE_HACKATHON_AIG.json) |
| C — Local Docker | PASS, generic capability only | Linux Docker Desktop/WSL2 kernel, cgroup v2; actual controls, stopped/removed owned container, no leaked scratch, ten pre-existing container IDs preserved. [Final smoke](evidence/PRE_HACKATHON_DOCKER.json) |
| D — Account/credits | Assessed; USER_ACTION_REQUIRED / PENDING | No enabled browser/app surface and no recognized process key; no account inference. Official offer $200; coupon still pending on public page. [Account checklist](../VULTR_ACCOUNT_CHECKLIST.md), [reference evidence](evidence/PRE_HACKATHON_REFERENCES.json) |
| E — Compute/cost | PASS, plan only | Three catalog candidates compared, one recommendation/one fallback, actual public capacity read, 151-hour estimate and $50 proposed ceiling. [Resource plan](../VULTR_RESOURCE_AND_COST_PLAN.md) |
| F — Inference | PASS, plan only | Actual unauthenticated 26-model catalog; current exact IDs/limits/features/prices and documentation conflicts recorded. No authenticated or paid request. [Catalogs](evidence/PRE_HACKATHON_PUBLIC_CATALOGS.json) |
| G — Deployment operations | PASS, procedure only | Concrete Caddy/owned-subdomain/systemd/path/firewall/persistence/rollback/shutdown procedure; remote host/TLS/browser proof NOT RUN. [Runbook](../DEPLOYMENT_RUNBOOK.md) |
| H — Compliance | PASS, public-source checks only | Dates unchanged; general reuse treatment LOW; public repo verified; enrollment, individual eligibility and final form unverified. [Competition readiness](../COMPETITION_READINESS.md) |

Commands genuinely run include:

```powershell
uv venv --python D:\anaconda3\python.exe .venv
uv lock
uv sync --locked
uv sync --locked --offline --link-mode copy
uv lock --check --offline
uv pip check --python .venv/Scripts/python.exe
.venv/Scripts/python.exe -I scripts/preflight/environment.py --output docs/PHASE_REPORTS/evidence/PRE_HACKATHON_ENVIRONMENT.json
.venv/Scripts/python.exe -I scripts/preflight/verify_aig.py --output docs/PHASE_REPORTS/evidence/PRE_HACKATHON_AIG.json
docker --context desktop-linux pull alpine:3.23
.venv/Scripts/python.exe -I scripts/preflight/docker_smoke.py --context desktop-linux --image alpine@sha256:85fe1e81d6758c208f3e1eed4338a1997e19d4be002d4dd32d3100c9a8c010a0 --output docs/PHASE_REPORTS/evidence/PRE_HACKATHON_DOCKER.json
ruff check scripts/preflight
ruff format --check scripts/preflight
git diff --check
```

`uv lock` resolved 24 packages including the virtual root; **23 distributions installed**, no conflicts. A fresh temporary project-local environment also synchronized offline from the same lock, imported the pinned installed public API with `-I`, passed `uv pip check` and was removed. A separate negative CLI check rejected `alpine:latest` with exit 2 before any Docker call. Ruff 0.12.0 and syntax checks passed. Actual exit codes/output, tag object/peeled commit and ignore checks are retained in [command evidence](evidence/PRE_HACKATHON_COMMANDS.json). The initial cache hardlink warning was handled by `--link-mode copy`; no global configuration changed. Linux lock installation is a future M1 host check, not proved by Windows success.

Local Docker observations: UID 65534, read-only root, disposable read-only marker bind with denied writes/unchanged host hash, writable bounded tmpfs, zero effective capabilities, `NoNewPrivs=1`, seccomp mode 2, no injected host env/socket/ports, CPU cgroup `25000 100000`, memory 67,108,864 bytes, swap zero, PID maximum 32. Only loopback was present and a bounded external TCP attempt failed under `network=none`. Stop completed in **1.621 s**, exit 137, `OOMKilled=false`; independent inventory found no remaining scoped container. No user network/volume was created, no unrelated container was removed, and the downloaded official image remains as a local cache entry. Stress, escape, internal bridge/host/metadata/IPv6 isolation and all Vultr tests are **NOT RUN**.

Three smoke attempts are retained: [attempt 1 FAIL](evidence/PRE_HACKATHON_DOCKER_ATTEMPT_1.json) exposed Windows CRLF in a benign marker; its container/scratch were removed. The script now writes exact LF bytes. [Attempt 2 PASS](evidence/PRE_HACKATHON_DOCKER_ATTEMPT_2.json) verified that correction. The final PASS followed a Linux-portability/scratch-permission and image-env check improvement. These are script-qualification iterations, not incident experiments or cherry-picked recovery samples. Backend overlay paths are omitted in the first record; no credentials were collected.

Five public provider GETs returned 200 (plans, regions, two capacity lists and model catalog). Public GitHub repository metadata returned `private=false`, branch `main`, no detected license. The rule book's embedded MDX was inspected as text, not executed. Official web references and catalog subset hashes are recorded; raw public responses are retained locally under ignored `.local/public-sources/`. A catalog request never verifies a key, credits, model quality or deployed inference.

## B. Exact created/modified files

Created environment/configuration:

```text
.env.example
.gitignore
.python-version
pyproject.toml
uv.lock
```

Created generic scripts:

```text
scripts/preflight/environment.py
scripts/preflight/verify_aig.py
scripts/preflight/docker_smoke.py
```

Created preparation documents:

```text
docs/COMPETITION_READINESS.md
docs/VULTR_ACCOUNT_CHECKLIST.md
docs/VULTR_RESOURCE_AND_COST_PLAN.md
docs/PHASE_REPORTS/PRE_HACKATHON_READINESS_REPORT.md
```

Updated current guidance only:

```text
docs/AIG_VERSION_DECISION.md
docs/DEPLOYMENT_RUNBOOK.md
docs/ORIGINALITY_AND_REUSE.md
docs/REQUIREMENTS_TRACEABILITY.md
```

Created sanitized evidence:

```text
docs/PHASE_REPORTS/evidence/PRE_HACKATHON_AIG.json
docs/PHASE_REPORTS/evidence/PRE_HACKATHON_COMMANDS.json
docs/PHASE_REPORTS/evidence/PRE_HACKATHON_DOCKER.json
docs/PHASE_REPORTS/evidence/PRE_HACKATHON_DOCKER_ATTEMPT_1.json
docs/PHASE_REPORTS/evidence/PRE_HACKATHON_DOCKER_ATTEMPT_2.json
docs/PHASE_REPORTS/evidence/PRE_HACKATHON_ENVIRONMENT.json
docs/PHASE_REPORTS/evidence/PRE_HACKATHON_PUBLIC_CATALOGS.json
docs/PHASE_REPORTS/evidence/PRE_HACKATHON_REFERENCES.json
docs/PHASE_REPORTS/evidence/PRE_HACKATHON_VALIDATION.json
```

The ignored `.venv` and `.local` contain the environment, scratch research and validation helpers; they are not delivery/source artifacts. No product modules, frontend, incident fixture or worker exist. Root `AGENTS.md`, README, Master Design, ADR-009, threat model, original P0 report/evidence and upstream AIG source remain unchanged. Final scope, Markdown fences/local links/JSON syntax, bounded secret-shape scan and hash inventory: [validation](evidence/PRE_HACKATHON_VALIDATION.json). The scan is not a complete secret audit. No files are staged; no commit/push occurred in this sprint.

## C. Recommended Vultr configuration

One `vhp-4c-8gb-amd` Sydney VM (4 vCPU, 8,192 MB RAM, 180 GB disk) at catalog $0.066/hour/$48 monthly; fallback `vc2-4c-8gb` Melbourne at $0.055/hour/$40 monthly. Public capacity lists contained both at check time; recheck the actual console/account before creating one. Caddy + one FastAPI/AIG owner + separate trusted worker + two SQLite stores + local immutable artifacts; API has no Docker access. Primary inference `qwen3.8-27b`, deliberately selected fallback `minimax-m3`, both through Vultr. All live quality/authentication/latency is unverified.

151 hours plus bounded inference/network reserve and 50% contingency is **about $17 before unquoted tax/domain/subscription conditions**. Proposed maximum remains $50, never an authorization. Credits do not reduce the cash-liability estimate until actual applicability is confirmed. Hosting after the proposed Nov 10 shutdown needs a judge-availability decision and updated quote. See the [cost calculation](../VULTR_RESOURCE_AND_COST_PLAN.md#cost-calculation-and-ceilings) and its official source links.

## D. Consolidated user actions

Complete the [single external-action checklist](../VULTR_ACCOUNT_CHECKLIST.md#consolidated-user-actions): registration/eligibility/team, Vultr account/email/payment, eventual event-coupon terms/redemption, existing API/inference access, private credential custody, owned subdomain/SSH access, operation-specific resource/call budget/end-time approval, judge hosting duration and owner-granted MIT license. Do not paste keys/payment data into chat. No need to obtain an organizer answer about ordinary AIG reuse before doing permitted preparation.

## E. Remaining material risks and future security acceptance

No observed public-API/architecture blocker requires redesign before M1. The following are execution/prerequisite gates, not achieved product behavior:

| Gate | Exact action / evidence needed |
|---|---|
| Account/credits/quota | Complete checklist; inspect console availability/limits and actual promotion terms; use an explicitly approved cash budget only if chosen |
| Inference drift and mixed documentation | Quote subscription charges, rediscover exact model ID and make one authorized generic call; reject wrong/missing model, invalid/partial output and timeout; never auto-fallback/retry |
| Real host isolation | M1 verifies Linux install, cgroup/privilege controls, scoped termination/teardown and port boundaries; M2/P1 qualifies actual internal-network/host/metadata/IPv4/IPv6/DNS denial and secret/socket/host-marker controls before relying on sandbox execution |
| Replay and privileged worker | Qualify fixed workload and host headroom after kickoff; trusted Docker worker is root-equivalent; actual worker/queue/race/Unknown/approval tests belong to authorized P2/P3, still NOT RUN |
| Public HTTPS and demo retention | Confirm domain/SSH, real external browser and mutation denials; agree hosting period before final destruction; a guest stop does not stop billing |
| Eligibility and licensing | Personal/event form checks remain; preserve full AIG MIT notice and grant product license before release; no organizer approval is claimed |

The future sandbox suite must cover all [CT-01–10](../THREAT_MODEL.md#required-attack-and-fault-experiments): host marker, wall-clock termination, forbidden patch, hostile logs, secret/socket absence, actual egress canaries, bounded memory/PID/CPU stress with healthy control plane, worker lifecycle crash/quarantine, artifact/trial/receipt tampering and lost enqueue acknowledgment. Equal-condition replay and independently verified teardown are mandatory. No infinite loop, malicious payload, exploit, Kubernetes or product fault case was run during preparation. A passing generic `network=none` test cannot establish the future internal-network policy or universal containment.

Security decisions preserved: exact immutable AIG dependency, one future governed short enqueue/default five-second budget, separate approval/authorization, HELD until verified AIG Succeeded, independent worker states, no unknown-effect replay, private operator/public result separation, no sandbox secrets/socket, no pre-kickoff core implementation. Configuration remains explicit and future state is not provisioned automatically.

## F. Kickoff sequence

At **2026-11-04 04:00 NZDT**, first re-read the [official live milestones](https://lablab.ai/ai-hackathons/vultr-hackathon/live) and event page. Confirm the window is open; dates remain subject to organizer updates. From this repository:

```powershell
git status --short --branch
Get-Content AGENTS.md
Get-Content docs/COMPETITION_READINESS.md
Get-Content docs/VULTR_ACCOUNT_CHECKLIST.md
Get-Content docs/VULTR_RESOURCE_AND_COST_PLAN.md
Get-Content docs/DEPLOYMENT_RUNBOOK.md
uv sync --locked
uv lock --check --offline
uv pip check --python .venv/Scripts/python.exe
.venv/Scripts/python.exe -I scripts/preflight/verify_aig.py --output .local/aig-kickoff.json
```

Then: complete external user actions → obtain exact **M1/P0-only** resource/call authorization → provision one quoted VM → secure SSH/firewall/users → transfer reviewed source/lock → install/verify Linux environment → qualify harmless Docker lifecycle → configure owned DNS/Caddy/HTTPS → perform one separately approved generic Vultr connectivity request → verify public browser/read-only safety → retain real evidence and report M1/P0. The runbook contains future host commands; none ran here. Do not start incident/agent/worker implementation or automatically advance to M2/P1 under this preparation instruction. No placeholder application entrypoint should be executed.

## G. Recommendation

**The project can remain frozen until kickoff.** All possible authorized local preparation and public research work is complete; the user can complete the listed external prerequisites without further architecture work. M1 remains conditional on the official window and specific resource/call authorization. Cloud deployment, real inference and product/containment correctness remain NOT RUN.

Next authorized phase when requested: **M1 / repository P0 infrastructure reality only**. Recommended model: **Codex Sol, High**, with **Extra High** for actual sandbox/network and AIG trust-boundary review. No automatic phase advancement, commit, push, cloud spend or publication.
