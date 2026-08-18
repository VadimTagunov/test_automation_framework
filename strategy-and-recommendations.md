# Strategy & Recommendations

## Why these 2 tests were chosen for automation

**UI E2E — successful single bet placement.** Out of the 6 scenarios in the test plan, this is the
only one that is a pure, unconditional happy path with no branching outcomes to assert against. That
matters specifically for UI automation: Selenium tests are the most expensive to write and maintain
(brittle locators, timing/waits, browser overhead), so they earn their cost best on the one journey
that is both highest business value (it's the entire revenue-generating flow) and simple enough to
assert deterministically end-to-end — select match, select odds, enter stake, submit, verify receipt.
Scenarios like the duplicate-submission race condition (TC-05) or live balance updates were
deliberately *not* chosen for UI automation, even though they're arguably higher severity, because
they are timing-dependent and intermittent by nature — a Selenium test asserting on race-condition
timing would itself be flaky, which defeats the purpose of a reliable regression suite.

**API — stake below minimum rejected with `422 invalid_stake_min`.** This was chosen over the other
validation candidates (missing selection, invalid match ID, stake precision, insufficient balance)
because it's the cleanest example of a pure business-rule check: no dependency on account balance
state, no dependency on match catalog contents, a single deterministic request/response pair,
straight from the documented OpenAPI contract. Validation rules like this are exactly the kind of
check that should live at the API layer rather than the UI layer — the UI already blocks this stake
range client-side, but the API test is what actually proves the business rule is enforced
server-side and can't be bypassed by a client that skips UI validation entirely (as a malicious or
buggy client could).

## What was intentionally left manual-only, and why

- **The duplicate-submission race condition (BUG-04).** This is the most severe defect found, but
  it is inherently non-deterministic — reproducing it reliably in an automated test would require
  either flaky timing assumptions or artificial throttling that doesn't reflect real user behavior.
  It's better suited to targeted load/concurrency testing (e.g. firing near-simultaneous requests via
  a script or a tool like Locust) as a follow-up investigation, not a pass/fail regression test in
  the day-to-day suite.
- **Receipt payout/team-order consistency across many odds combinations (TC-06).** The UI test
  covers this once, on the happy path. Exhaustively checking it across many matches/odds is high
  manual-testing value (pattern detection — "is this systemic or a one-off?") but low automation
  value relative to effort, since it's the same assertion repeated with different data, not a new
  code path.
- **Filters (date range, odds range) and match list sorting/PAST-match visibility.** These weren't in
  the top-3 executed scenarios, and are more exploratory/UI-state-driven checks (dropdown behavior,
  visual sort order) that are cheap to verify manually but comparatively fiddly to automate
  reliably against a UI whose component structure wasn't inspected in depth for this assessment.
- **Error modal retry flow (network failure → error modal → Rebet/Close).** Requires reliably
  forcing a `500`/network failure, which typically means intercepting network requests
  (e.g. via `selenium-wire` or a proxy) — reasonable to add later, but adds a new tooling dependency
  that wasn't justified for a 2-test scope.

## Recommendations if this project scaled

1. **CI/CD integration.** Run the `api` marker suite on every commit/PR (fast, no browser, easy to
   parallelize) and the `ui` suite on a schedule or pre-merge gate (e.g. GitHub Actions with a
   headless Chrome runner), publishing the Allure report as a build artifact. API tests catching
   business-rule regressions early, combined with a smaller, slower UI smoke suite, keeps feedback
   fast without sacrificing coverage of the critical journey.

2. **Add a dedicated concurrency/load-testing layer.** Given BUG-04 is the highest-severity finding
   and is fundamentally about server-side race conditions, the next investment after this assessment
   should be a lightweight concurrency test layer (e.g. a script firing N parallel `place-bet`
   requests for the same user and asserting exactly one succeeds) — sitting alongside, not replacing,
   the functional API/UI suites. This is also where balance-consistency checks (BUG-02, BUG-05) would
   naturally get automated regression coverage instead of remaining manual.

3. **Request spec clarification and treat the OpenAPI contract as the source of truth.** This
   assessment surfaced at least two direct contradictions between the PDF spec and the live API
   behavior/contract: minimum stake documented as both €1.00 (Business Rules) and €1.01 (Validation
   Rules) — resolved here by trusting the verified Swagger contract (€1.00) — and the odds filter's
   UI range (1.00–10.00) versus the documented business rule range (1.01–1000.00). At scale, this
   kind of drift compounds fast across a growing test suite; the recommendation is to designate the
   OpenAPI spec as the single source of truth for validation boundaries going forward, with the
   product spec linking to it rather than duplicating numbers that can silently diverge.
