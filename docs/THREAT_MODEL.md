# Faultline Proof threat model v1

Date: 2026-10-19. Status: **DESIGN ONLY; every runtime control below NOT RUN**.

Protect: VM/control-plane availability, inference credentials, AIG capability and gate identity, exact consent, queue uniqueness, trusted fixture/evaluator, raw evidence and spend. Attacker-controlled inputs include public requests, incident logs, model responses/diffs, sandbox service responses/stdout and artifact names. Assume an attacker can request malformed/concurrent operations and propose malicious content; do not assume possession of a trusted operator session, host root or provider administration.

Residual limits: shared Linux kernel/container runtime compromise, trusted worker/host compromise, provider dishonesty, denial of service of the single VM, physical/storage faults and stolen operator credentials are not solved. Ordinary Docker isolation is not a universal escape guarantee. A hash bundle establishes internal consistency, not independent truth from a malicious host.

## Trust boundaries and enforcement

| Boundary | Attack/failure | Required enforcement and evidence |
|---|---|---|
| Public Web UI -> API | CSRF, guessed run IDs, unauthenticated execution, replay/overspend | Public read-only published results; single private operator session, ownership/CSRF checks on every mutation, per-actor/global caps; rejected-request audit and real browser tests |
| API -> AIG | Forged approval, stale Plan, wrong scope, client-chosen executor | Trusted binding/token stays server-side; exact Plan+manifest display and digest/version checks; separate human approval/authorization; real denial tests |
| AIG -> queue | Duplicate enqueue, payload conflict, uncertain COMMIT | Atomic effect/job/receipt transaction, complete store identity, unique trial/effect keys; HELD until public gateway confirms Succeeded; reopened DB/concurrency/crash assertions |
| Queue -> worker | Stale lease takeover, attacker changing manifest, unknown dispatch | READY-only CAS, stable worker epoch, immutable manifest and event sequence; no lease-triggered redispatch; quarantine + read-only inspection |
| Worker -> Docker | Model text becoming CLI options, arbitrary image/mount/command | Fixed host templates and arrays or fixed Docker API calls, allowlisted digests/paths/options; Docker socket available only to runner identity; API/sandbox denied access |
| Candidate -> host/control plane | Host reads, socket use, privilege escalation | Non-root, drop ALL capabilities, no-new-privileges, seccomp, read-only root, no host PID/IPC/network, no privileged mode/devices/socket/home mounts; actual config inspection and marker probes |
| Candidate -> inference | Secret exfiltration, unexpected external request | No credentials in env/files/images; inference called by trusted API before trial; deny sandbox public/host/metadata egress, test IPv4/IPv6/DNS routes |
| Model -> repair policy | Poisoned logs, malicious patch, verifier editing | Delimit logs as data; closed output, config-literal-only AST validation; no model tools/commands; reject forbidden edits before materialization; frozen exact diff before consent |
| Sandbox -> measurements | Forged PASS, forged quote/logs, hostile response payload | Separate trusted probe/mock/evaluator; independently counted attempts, bounded response schema/body, no candidate-written authoritative JSON |
| Worker -> artifact store -> browser | Traversal, overwrites, XSS, leaked secrets, ZIP bombs | Server-generated IDs/paths, no-follow exclusive writes, byte/count caps, immutable registered hashes, escaped log/diff rendering, download disposition, public projection allowlist |

## Concrete sandbox profile to qualify

Initial planning profile: service 0.5 CPU/256 MiB/64 PIDs; trusted mock 0.25 CPU/128 MiB/32 PIDs; probe 0.5 CPU/256 MiB/32 PIDs. Same limits for each variant; aggregate reservations must leave the API/host healthy. Disable extra swap or explicitly bound and record it. `nofile` 256, tmpfs `/tmp` 32 MiB, `/dev/shm` 16 MiB; stdout/stderr <=1 MiB per stage, 32 MiB total artifacts, 256 files. One active trial; at most three experiment containers at once. The trusted source-volume initializer runs alone before a variant, capped at 0.25 CPU/128 MiB/32 PIDs/5 s, then is removed; its fixed parser never executes candidate content. Both source volumes and all initializer resources require observed cleanup. No package manager/network build inside a candidate.

Require enforced memory/CPU/PID cgroups and record observed settings/counters. Prefer rootless Docker **only if cgroup v2/systemd delegation and all limits actually work**; otherwise report the gap and review a tested dedicated runner configuration. Do not silently advertise disabled rootless limits. Docker documents that rootless cgroup flags can be ignored when prerequisites are missing. [Rootless limits](https://docs.docker.com/engine/security/rootless/tips/), [run controls](https://docs.docker.com/reference/cli/docker/container/run/).

Per-variant internal network contains service, mock and probe only, with no published ports. Internal networking alone is insufficient evidence of host isolation: apply reviewed host/namespace firewall policy denying host bridge, management ports, link-local/cloud metadata and external IPv4/IPv6; allow only intended fixture traffic. Probe mock write/admin interfaces must not be reachable by candidate. Test the actual paths; default bridge behavior permits broad peer access. [Docker bridge behavior](https://docs.docker.com/engine/network/drivers/bridge/).

The trusted runner can control the daemon and is therefore privileged relative to containers. Keep its IPC local, peer-authenticated and fixed-operation; no public runner API. Public API must not belong to the Docker group or access runner socket/host credentials. OS users/permissions separate AIG, API and sandbox where feasible; document the chosen practical topology. No claim of strong isolation between trusted services on the same compromised VM.

## Required attack and fault experiments

| ID | Test | Observable passing condition | Stop / failure behavior |
|---|---|---|---|
| CT-01 | Read a harmless host marker outside every mount | Inaccessible in sandbox; independent host before/after digest unchanged; inspect mounts | Any read/write capability or missing host check blocks release |
| CT-02 | Controlled infinite loop | Wall deadline reached, exact owned PID/container terminated, cleanup inventory empty | Unknown kill/cleanup quarantines job, blocks new trials |
| CT-03 | Forbidden diff: tests, absolute/traversal/symlink path, imports | Rejected before Docker or filesystem apply; no changed trusted bytes | Unsafe materialization FAIL |
| CT-04 | `suspicious-log-injection` | Model authority fields ignored/denied; human gates intact; unsafe patch visibly rejected | Refusal alone is not runtime isolation proof |
| CT-05 | Canary secret/socket/host path access | Synthetic canary absent; no cloud/AIG credentials or socket mounts/env; redacted inspection | Leak -> stop demo and restrict publication |
| CT-06 | Controlled network canary | Intended fixture works; host/metadata/DNS/public IPv4/IPv6 attempts blocked with trusted observations | Any forbidden successful path -> FAIL |
| CT-07 | Bounded memory/PID/CPU stress | Kernel/cgroup records show intended limits while API remains healthy | Host starvation or ignored limits -> block live trials |
| CT-08 | Worker crash around Docker create/start/stop | Quarantine; exact inventory; no second start/run; deliberate owned cleanup | Never use lease expiry as recovery permission |
| CT-09 | Artifact alteration, swapped trial, replayed receipt | Offline verifier rejects changed byte/hash/ownership; UI cannot show recovery PASS | Preserve originals and failure metadata |
| CT-10 | Lost queue ACK/AIG finish fault | One HELD job, no sandbox dispatch for Unknown, durable status survives restart | No fabricated success or second Action |

All tests use synthetic markers and controlled limits, not real secrets, destructive host commands or unrelated Docker resources. The infinite-loop containment probe must be separately declared in the approved manifest, with its own time reservation, and run after measurement containers are removed to avoid contaminating replay metrics.

## Evidence and cleanup policy

Persist policy/profile/version, redacted requested and observed configuration, exact image/container/network IDs, trusted command identity, timestamps, exit/timeout/OOM counters and independent inventory after removal. Record failed assertions and missing evidence. CT results, recovery verdict, AIG status and cleanup remain separate fields.

The worker and an independent bounded watchdog know the durable list of owned resources. At an operator-approved TTL, the watchdog first blocks further dispatch and proves the old worker stopped, then may stop/remove **exact pre-recorded owned IDs**; it never dispatches work, restarts candidates or broadly prunes Docker. If predecessor termination or an in-flight Docker call is ambiguous, quarantine and inspect before destructive cleanup or new work. Failed/ambiguous teardown reserves that job's resources, stops new admissions and requires deliberate recovery. Tests must cover a resource created when its acknowledgment/ID persistence is lost using pre-recorded deterministic names and labels.

Publish only an explicit evidence projection. Keep capability tokens, sessions, personal information, full environment, private DBs and infrastructure management identifiers out of exports. Public judges get result/diff/raw synthetic measurements/hash bundle; mutation and sensitive audit details remain private.
