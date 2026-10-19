# Vultr account and operator checklist

Verified: 2026-10-19, Pacific/Auckland. **USER_ACTION_REQUIRED.** No connected browser/app surface was available in the computer-use inventory, and no recognized Vultr credential was present in the execution process. This does not mean the user has no account or no locally stored keys. No home-directory credential search, account login, private account API request, registration, payment, key change or redemption was performed.

## Observed readiness

| Item | Status | Evidence / next manual check |
|---|---|---|
| Account exists / email verified | UNVERIFIED; USER_ACTION_REQUIRED | Sign in at [Vultr Console](https://console.vultr.com/); verify profile/email state |
| Billing/payment setup | UNVERIFIED; USER_ACTION_REQUIRED | Account → Billing; inspect verified payment method without sharing financial details |
| Account credit amount / expiry | UNVERIFIED; USER_ACTION_REQUIRED | Account → History under Billing; inspect credit entry and applicable terms |
| Hackathon allocation | CONFIRMED as a published offer, not personal entitlement | [Event page](https://lablab.ai/ai-hackathons/vultr-hackathon) advertises $200 per participant |
| Hackathon coupon / redemption | PENDING | Event says code will be published before kickoff; no code invented or redeemed |
| Credit applicability | EVENT-SPECIFIC UNVERIFIED | Confirm Compute **and** Inference coverage, expiration, eligibility for existing customers, geography and stacking restrictions against the actual offer |
| Management API enabled / key exists | UNVERIFIED; USER_ACTION_REQUIRED | Account → API; inspect state without creating/rotating a token |
| Recognized process credentials | MISSING | `VULTR_API_KEY`, `VULTR_API_TOKEN`, `VULTR_INFERENCE_API_KEY`, `VULTR_INFERENCE_KEY`; values never printed ([environment evidence](PHASE_REPORTS/evidence/PRE_HACKATHON_ENVIRONMENT.json)) |
| Inference subscription / key / quota | UNVERIFIED; USER_ACTION_REQUIRED | Products → Serverless → Inference; inspect an existing subscription's Overview/Usage; adding one incurs charges and is outside this sprint |
| VM/account restrictions | UNVERIFIED; USER_ACTION_REQUIRED | Inspect account resource limits and permitted region/plans before provisioning |
| Public plan/model catalog | PASS, unauthenticated reads only | [Actual public GET evidence](PHASE_REPORTS/evidence/PRE_HACKATHON_PUBLIC_CATALOGS.json); not account access proof |

## Redemption and account procedure

The [official account guide](https://docs.vultr.com/platform/create-an-account) describes email verification and billing setup. If an account is needed, the user completes signup, terms and payment verification directly. The [payment-method requirement](https://docs.vultr.com/support/platform/billing/why-do-i-need-to-enter-a-payment-method) applies before deployment. Do not treat credits as removing payment verification or liability.

When the event publishes its actual code, read those terms first, then the user can navigate to Account/Billing → Gift Code (or the coupon field in the onboarding Summary) and redeem it. Vultr's [general promotion guide](https://docs.vultr.com/support/platform/billing/how-can-i-add-a-promotional-code) requires a linked valid card or PayPal, limits general promotions to one per user and says credits expire. Those generic conditions do not establish the hackathon offer's exact expiry, stacking, service or regional terms. The event links a redemption video but still says the code is pending; no personal credit balance is verified. Avoid redeeming a different generic promotion that might consume eligibility for this offer.

To verify credits, [Account → History](https://docs.vultr.com/platform/billing/view-payment-history) shows balance/charges; inspect the specific promotion's expiry/coverage and retain a private dated note. Record only CONFIRMED/UNVERIFIED and non-sensitive terms in repository evidence, not invoices, payment details or account identifiers.

For inference, Products → Serverless → Inference is the [documented provisioning path](https://docs.vultr.com/products/compute/serverless-inference/provisioning). Inspect existing subscriptions first. Adding a subscription acknowledges supported models and charges; defer that mutation until explicitly approved. Keep the inference subscription key separate from the infrastructure management key. A public `/v1/models` response is not an authentication test.

## Credential handling

Use a trusted password/secret manager or an OS-protected private directory outside the repository. For the future Linux service use root-protected systemd credentials, readable only by the intended API service; keep management credentials on the operator workstation. No management API key is required inside a sandbox or the deployed application. The worker does not receive inference credentials or the AIG capability. The actual app credential-loading code is intentionally not implemented yet.

`.env.example` contains empty placeholders; `.env`, `.env.*` (except the example), `.local`, private keys and SQLite state are ignored. Git ignore is an accident-prevention measure, not secret storage access control. Never include real values in tracked config, commands captured by a transcript, screenshots, frontend bundles or reports. Preflight records presence only, never a token fragment/hash. Do not paste keys into chat. If a key is found exposed later, stop publication and let the user rotate it through the console.

Inspect Account → API → Access Control for the approved workstation IP. [Product-scoping guidance](https://docs.vultr.com/support/platform/api/can-i-scope-api-keys-to-specific-products) describes user/ACL controls rather than arbitrary invented per-key scopes. Do not click “Allow all IPv4” or create permissions as part of this readiness check. Any key generation, permission change or subscription creation requires a later explicit instruction; the current absence of a process variable is not permission to create one.

## Consolidated user actions

These are the remaining external prerequisites; independent local/research work is complete. No secret values need to be sent back to chat.

- [ ] Confirm lablab registration, Discord connection, team (1–6) and personal/prize eligibility before registration closes. Use the [competition checklist](COMPETITION_READINESS.md).
- [ ] Sign in to Vultr; confirm account/email/payment verification and regional/account resource restrictions. Finish any signup/terms/payment steps personally if needed.
- [ ] When released, inspect and redeem the **event** coupon yourself; record amount, expiry, Compute/Inference coverage and existing-account restrictions privately. If unavailable, choose whether to use a separately approved cash budget; no automatic assumption of free usage.
- [ ] Confirm an existing management key and restricted access configuration if API-based provisioning is chosen. Keep it in the secret manager; console provisioning is sufficient and does not require creating a management key just for this demo.
- [ ] Inspect Inference subscription/charges and key availability. Authorize adding one only if needed; store its credential privately and make it available only to the trusted API service when deploying.
- [ ] Identify an existing owned subdomain, DNS control and the operator's SSH source IP/public key. No DNS or SSH credential changes were made here.
- [ ] At kickoff give operation-specific authorization for the exact VM/region, inference allowance, spending ceiling and end time in the [resource plan](VULTR_RESOURCE_AND_COST_PLAN.md). Confirm judges' required hosting duration and who will perform/approve final destruction. The $50 proposal is not authorization.
- [ ] Confirm the product MIT license grant and third-party notice inclusion before public release. No license was granted on the user's behalf during preparation.

Organizer clarification about unchanged AIG reuse is optional additional assurance. Its current **LOW — Pending Event-Specific Confirmation** rating does not gate these preparation steps. Official event-specific rules remain authoritative.
