# Competition readiness and freeze boundary

Checked: 2026-10-19, Pacific/Auckland. **PUBLIC RULES CHECKED; personal enrollment/eligibility UNVERIFIED; deployed product NOT RUN.** This is a pre-hackathon environment/readiness record. It does not authorize M1/P0, cloud spend or submission.

## Schedule and precedence

The [official live dashboard](https://lablab.ai/ai-hackathons/vultr-hackathon/live) still gives kickoff **2026-11-03 15:00 UTC = 2026-11-04 04:00 NZDT**, and cutoff **2026-11-08 22:00 UTC = 2026-11-09 11:00 NZDT**. Registration closes at kickoff. Build window: **127 hours**. Internal submission target stays **2026-11-08 20:00 NZDT**. Ignore the dashboard's zero countdown; use explicit milestone text. The event overview's detailed schedule is still TBA. Recheck official milestones before starting, spending or submitting.

The event page and actual submission form take priority over general guidance. The [rule book](https://lablab.ai/hackathon-rules) was retrieved from the page's embedded MDX source because its text-only rendering was empty; it also gives form/event precedence. No private registration/submission form was accessed. Do not use its general grace period as the deadline.

## Requirement matrix

| Item | Classification | Current result / action |
|---|---|---|
| Online participation; team 1–6 | CONFIRMED public rule | [Event](https://lablab.ai/ai-hackathons/vultr-hackathon); personal participation, profile/Discord and team registration USER_ACTION_REQUIRED |
| Personal/residency/prize eligibility | EVENT-SPECIFIC UNVERIFIED for this user | User verifies participant terms and any prize restrictions; welcome text is not eligibility approval |
| Vultr VM backend and Serverless Inference for agent LLM calls | CONFIRMED | Planned; actual cloud execution/authentication NOT RUN |
| External sandbox execution on Vultr; process/secret/resource/lifecycle controls | CONFIRMED | Local generic Docker smoke PASS; Vultr execution/containment NOT RUN |
| Original MIT-compliant submission | CONFIRMED | Competition-specific core remains unimplemented; product LICENSE still to be granted by owner |
| Pre-existing MIT AIG dependency | GENERALLY ALLOWED; event-specific approval UNVERIFIED | **LOW — Pending Event-Specific Confirmation**; exact v0.2.0 pin and attribution retained |
| Core AI functionality developed inside allowed window | GENERALLY REQUIRED by published reuse guidance; stronger repository boundary retained | No Faultline agent/incident/worker/frontend/replay/evaluator code authored in this sprint |
| Public GitHub/setup documentation | CONFIRMED requirement | [Public repository](https://github.com/miku-wwl/faultline-proof) API reports `private=false`, default `main`; this sprint remains local/uncommitted, product setup not yet implemented |
| Public browser demo with working product flow | CONFIRMED requirement | HTTPS plan prepared; real public app NOT RUN |
| Video with one actual containment moment | CONFIRMED requirement | No recording or sandbox-security claim from preflight |
| Cover and slide presentation | CONFIRMED event submission items | To be made during product/submission phase |
| Video within five minutes, under 300 MB; title/description limits | GENERAL GUIDANCE; event form UNVERIFIED | [Submission guide](https://lablab.ai/ai-articles/hackathon-guidelines); final form controls |
| Additional tracks/partner requirements | EVENT-SPECIFIC UNVERIFIED | Still TBA; recheck official announcements |
| Public offer of $200 credits | CONFIRMED offer only | Coupon PENDING; personal receipt, expiration and service coverage UNVERIFIED |
| Specific intended action explicitly prohibited by located event rules | No such additional prohibition identified | This is not a blanket permission or a finding of guaranteed eligibility |

The event findings above come from the [official competition page](https://lablab.ai/ai-hackathons/vultr-hackathon). The [general reuse guide](https://lablab.ai/guide/ai-hackathons) supports existing libraries/scaffolding while reserving core AI work for the event and deferring to event-specific rules. AIG is infrastructure governance, not the incident product. An organizer answer is optional assurance, not a prerequisite for toolchain/dependency preparation. Never claim organizer approval without evidence. The [originality inventory](ORIGINALITY_AND_REUSE.md) records the separation and required MIT notices.

## Work performed before kickoff

Allowed preparation completed under this sprint's explicit local authorization: project Python manifest/lock/environment, installed dependency integrity/API qualification, generic tool inventory, benign generic Docker controls/lifecycle test, public account/product/rules/pricing research, empty configuration template, and nonexecuting deployment procedures. No competition-specific adapter, incident, model client, queue/worker, frontend, sandbox runner or evaluator was implemented. Generic smoke code does not qualify as the product's containment suite.

The read-only root instructions and architecture contracts stay in force. The current installation supersedes the Phase 0 **absence of a consumer environment**, not its historical execution results. See [readiness evidence](PHASE_REPORTS/PRE_HACKATHON_READINESS_REPORT.md).

## Kickoff release checks

1. Re-read official live/event pages and actual enrolled team dashboard; confirm the window is open and no new track/eligibility conflict applies.
2. Complete the [single operator checklist](VULTR_ACCOUNT_CHECKLIST.md#consolidated-user-actions), including billing/credit/subdomain/host retention decisions; do not collect secrets in chat.
3. Start only explicitly authorized **M1 = repository P0 infrastructure reality** using the [runbook](DEPLOYMENT_RUNBOOK.md). Passing preflight does not authorize provisioning or paid calls.
4. Retain genuine VM/inference/HTTPS/sandbox evidence before calling that phase PASS. M2/incident work maps to P1 and needs its own phase instruction. Keep AIG single-tool/default-five-second semantics and all governance gates unchanged.
5. Before submission, check public links anonymously, owner-granted MIT license and AIG notices, complete current form fields, real containment video/slides/cover, artifact redaction and honest failure states. Preserve all attempts; no synthetic metrics or screenshot-only proof.

No organizer messages, registration, terms acceptance, credit redemption, publication or submission were performed. No further generic design/research phase is needed; freeze the prepared project until kickoff while the user completes external account actions.
