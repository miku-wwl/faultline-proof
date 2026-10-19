# Vultr resource, inference and cost plan

Verified: 2026-10-19, Pacific/Auckland. **PLAN READY; provisioning, paid inference and deployment NOT RUN.** Dollar amounts are USD before tax. This document proposes a budget; it does not authorize spending.

## Compute decision

Use one Ubuntu 24.04 LTS amd64 VM, public IPv4, local SSD, Caddy, host-supervised Python API/AIG and a separately supervised trusted Docker worker. Keep one active trial and baseline/candidate sequential. No GPU, Kubernetes, managed database, load balancer, object storage, paid backups or extra volume is needed initially.

The [public plans API](https://api.vultr.com/v2/plans?type=all) and [regions API](https://api.vultr.com/v2/regions) returned HTTP 200. Retained values and response hashes: [catalog evidence](PHASE_REPORTS/evidence/PRE_HACKATHON_PUBLIC_CATALOGS.json). The website pricing page returned 403 to the research browser, so these are actual API catalog values rather than a guessed website quote.

| Choice | Plan / region | vCPU / RAM | Local disk / monthly transfer | Catalog hourly / monthly | Decision |
|---|---|---|---|---|---|
| Recommended | `vhp-4c-8gb-amd`, Sydney `syd` | 4 / 8,192 MB | 180 GB / 6,144 GB | $0.066 / $48 | Headroom for API, worker, image cache and three bounded experiment containers; operator proximity to Auckland |
| Fallback | `vc2-4c-8gb`, Melbourne `mel` | 4 / 8,192 MB | 160 GB / 4,096 GB | $0.055 / $40 | Same capacity envelope, lower price; qualify shared-CPU timing before freezing replay |
| Considered, rejected for initial demo | `vhp-2c-4gb-amd`, Sydney | 2 / 4,096 MB | 100 GB / 5,120 GB | $0.033 / $24 | Less contention margin during builds, probes and public requests |

The unauthenticated [Sydney availability API](https://api.vultr.com/v2/regions/syd/availability?type=vhp) listed the recommended plan, and [Melbourne availability](https://api.vultr.com/v2/regions/mel/availability?type=vc2) listed the fallback at check time. These observations reserve no capacity and prove no account entitlement. Recheck immediately before creating **one** VM; never provision both as a speculative hedge. Inference catalog locations are separate from VM region selection; both selected models currently list `sea` (US), so cross-region latency remains unmeasured.

Keep the existing [threat-model resource profile](THREAT_MODEL.md): service 0.5 CPU/256 MiB, mock 0.25 CPU/128 MiB, probe 0.5 CPU/256 MiB, maximum three experiment containers and one trial. Initializer runs alone; containment probes run after measurement containers are removed. Reserve the remaining CPU/RAM for trusted services and OS. Local Docker checks do not establish Vultr performance or enforcement.

## Inference decision and protocol

Use only `https://api.vultrinference.com/v1`, with a separate Serverless Inference subscription key held by the trusted API process. No management key or inference key enters a sandbox. [Authentication documentation](https://api.vultrinference.com/docs/get-started/authentication) specifies bearer authentication and identifies the public `/v1/models` route as not requiring a key. A successful catalog GET therefore proves neither authentication nor subscription access.

| Candidate | Exact current ID | Input / output per million tokens | Catalog text context / output field | Role |
|---|---|---|---|---|
| Primary | `qwen3.8-27b` | $0.15 / $1.00 | 262,144 / 262,144 tokens | Compact coding-oriented candidate for one narrow configuration proposal |
| Deliberately selected fallback | `minimax-m3` | $0.20 / $0.90 | 524,288 / 524,288 tokens | Different coding/reasoning candidate if primary fails qualification |

IDs, prices and fields were retrieved from the [live catalog](https://api.vultrinference.com/v1/models) and agree with the [models/pricing page](https://api.vultrinference.com/docs/models). These are provisional engineering choices based on advertised coding suitability, bounded-output support and cost, **not observed latency, quality or reliability rankings**. The catalog advertises tools and JSON response formats for both; live feature qualification remains NOT RUN. No tool execution is required by this product's planning client. A fallback requires explicit trusted configuration and a new recorded call; no automatic switch or non-Vultr provider is allowed.

The [chat reference](https://api.vultrinference.com/docs/reference/create-chat-completion) documents `POST /v1/chat/completions`, `messages`, explicit `model`, output caps, optional tools and `response_format` (`text`, `json_object`, `json_schema`). Start with plain chat plus deterministic local validation. Provider JSON enforcement is optional assistance. Never omit `model`: the gateway can choose a default. Persist requested and returned identities; any mismatch/missing identity blocks admission until a reviewed alias mapping or provider issue is resolved. Record response ID, finish reason, UTC/monotonic timing, usage and response digest; model prose never supplies execution authority.

The [limits page](https://api.vultrinference.com/docs/concepts/limits) currently states 120 requests/minute/model/subscription, 16 concurrent requests and a 32,768-token default output limit, with lower model-specific limits possible; provider timeout is approximately nine minutes. The larger output fields in the catalog are not a safe consumer budget. Future host ceilings: 8,192 input tokens, 2,048 total completion tokens, one in-flight call, at most two explicit draft calls per operator per ten minutes, 100 calls and 8 KiB accepted proposal bytes for the event. Count reasoning in the completion allowance. These are planned local controls, not implemented or provider-enforced spend guarantees.

[Documented errors](https://api.vultrinference.com/docs/concepts/errors) include 400 malformed input, 401 inactive/missing key, 404 missing model/route, 413 size, 429 rate limit and 5xx provider failures. Record bounded sanitized errors and `Retry-After`; **do not automatically retry**. Planned client deadlines are 5 seconds to connect and 30 seconds total, with no redirects/retries and a bounded response. A timeout can still consume paid tokens. No partial/length-truncated response becomes an approved candidate.

### Nonexecuting connectivity example

This is a generic protocol specimen, not an executed request or an incident agent. Credential header is shown only as `Authorization: Bearer <redacted>`. Use `Content-Type: application/json` and the chat endpoint above.

```json
{
  "model": "qwen3.8-27b",
  "messages": [{"role": "user", "content": "Return a JSON object with status set to ready."}],
  "temperature": 0,
  "max_tokens": 64,
  "reasoning": {"enabled": false},
  "stream": false
}
```

At authorized M1/P0: (1) verify console charges/subscription and exact catalog ID; (2) load the inference credential into trusted process memory without printing it; (3) perform exactly one generic request with connect/total deadlines and retries disabled; (4) privately retain the bounded response, then publish only model/correlation/timing/usage/digest and a sanitized result; (5) verify HTTP success, exact model, complete output and schema. Failure is a failed connectivity check, never permission to retry or substitute a response. Test structured-output/configuration reasoning later during the permitted product phase with predeclared cases. **No request in this section was sent.**

## Cost calculation and ceilings

The verified window is 127 hours. Budget 151 VM hours from kickoff through a proposed shutdown at **2026-11-10 11:00 NZDT**: event plus 24 hours to collect evidence/finish operations. This shutdown is proposed, not authorized or scheduled. Confirm how long judges need the public demo before selecting the actual teardown time; extending beyond it requires an updated quote and approval.

| Item | Calculation / assumption | Estimate |
|---|---|---|
| Recommended VM | 151 × $0.066; attached disk included | $9.966 |
| Inference, 100 bounded calls | 819,200 input + 204,800 completion tokens, primary | $0.32768 |
| Fallback-priced upper estimate for the same 100 calls | 819,200 × $0.20/M + 204,800 × $0.90/M | $0.34816 |
| Network reserve | $0.01/GB × 100 GB **if billed as overage**; avoid assuming full-month transfer allowance for a short-lived VM | $1.00 |
| Additional storage / DNS / TLS | Local disk, an existing owned subdomain and Caddy; no new paid service | $0 incremental |
| Subtotal using higher inference estimate | $9.966 + $0.34816 + $1 | $11.31416 |
| 50% planning contingency | Tax, rate/rounding drift, extra verification; not a quote | $5.65708 |
| Rounded preparation estimate | Before unquoted taxes/domain purchases/subscription minimums | **about $17** |

Fallback VM for 151 hours is $8.305. One additional week at the recommended catalog rate adds $11.088 before tax. Recalculate if judges need longer hosting. A new domain is excluded; do not buy one or assume ownership. No confirmed monthly inference minimum/credit coverage exists for this user's subscription; console charges must be reviewed before adding it. A [March support article](https://docs.vultr.com/support/products/serverless/how-do-i-monitor-the-usage-and-cost-of-my-vultr-serverless-inference-subscription) gives different generic inference rates ($0.55/$2.75 per million); selected-model catalog rates are planning inputs, with the actual subscription quote controlling spend. At those generic rates the same token envelope costs $1.01376 and still fits the proposed allowance.

[Server billing documentation](https://docs.vultr.com/support/platform/billing/how-am-i-billed-for-my-servers) describes hourly rounding and a 672-hour monthly cap for non-GPU servers. Do not derive a replacement hourly price from that text or promise proration: catalog and final console invoice terms must be reconciled before approval. [Bandwidth overage](https://docs.vultr.com/support/platform/billing/what-is-the-bandwidth-overage-rate) is documented as $0.01/GB. Tax, account-specific prices, partial-month included transfer and optional add-ons remain quote-time checks.

Retain the existing **proposed $50 total ceiling**: $30 VM/storage/network, $10 inference, $10 contingency. Actual expected usage is substantially lower; none of these amounts is authorized now. Credit balances are excluded from the cash-liability estimate. Do not interpret a balance alert or local call counter as a hard provider spend stop. Before each new paid resource/call allowance, require a concrete quote, end time and owner; stop new work when the approved remaining budget is insufficient. Never automatically add a second VM or a second 100-call allowance.

## Naming, expiry and teardown

- VM label: `faultline-prep-20261104-<short-scope>`; one VM, maximum 4 vCPU/8 GiB, no unapproved add-ons. Store actual ID/scope/expiry privately.
- Trusted services: `faultline-api`, `faultline-worker`, Caddy; trial resources later use persisted UUID names and scope/job labels. No global Docker cleanup.
- At the approved end time block admission/model calls, stop the known worker and inventory exact owned resources. Quarantine ambiguous work; never redispatch for cleanup convenience.
- Remove only proved-owned trial containers/networks/volumes, confirm independent absence, preserve artifact hashes and a consistent SQLite backup including WAL handling, then stop services. Retain public evidence before VM removal.
- Obtain resource-specific destruction approval and destroy the exact VM through the console. Verify instances, any separately created storage/snapshots/reserved IPs and inference subscriptions; terminate only those included in that approval. [Stopped instances still bill](https://docs.vultr.com/support/platform/billing/are-stopped-instances-still-billed-on-vultr).
- Check Billing/History and inference Usage after deletion, record residual items/charges privately, and revisit delayed usage. Account-level charges unrelated to this scope remain untouched.

Account/credit steps and consolidated operator actions: [account checklist](VULTR_ACCOUNT_CHECKLIST.md). Future execution sequence: [deployment runbook](DEPLOYMENT_RUNBOOK.md). No Terraform apply, VM creation, DNS change or paid call occurred in this sprint.
