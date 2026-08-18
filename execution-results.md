# Execution Results & Bug Reports — Single Bet Placement

**Executed against:** https://qae-assignment-tau.vercel.app/ (user-id: `candidate-7PeYkDh0CI`)
**Browser:** Latest desktop Chrome
**Method:** Top 3 priority scenarios from `test-plan.md` executed manually, plus additional
exploratory testing around the bet placement flow, filters, and match list.

---

## Scope Note — TC-02, TC-03, TC-06

Per the assignment instructions, formal execution was scoped to the top 3 highest-priority scenarios
from the test plan — TC-01, TC-04, and TC-05, all rated Critical. TC-02, TC-03, and TC-06 (all High
priority) were not formally re-executed as standalone scenario runs, for the following reasons:

- **TC-06 (receipt data integrity)** overlaps directly with TC-01: placing a bet and inspecting the
  receipt is the same action either way, and the assertions TC-06 defines (team order, odds, payout
  consistency) are exactly what surfaced BUG-01 and BUG-03 during TC-01 execution. Running it again
  as a separate pass would have been redundant rather than additional coverage.
- **TC-02 (stake boundary/precision validation)** and **TC-03 (insufficient balance)** were partially
  covered during the initial exploratory pass (see reconnaissance notes): stake = 0, > €100, and > 2
  decimal places were confirmed blocked by the UI, and stake exceeding balance was confirmed blocked
  by the UI. However, this was informal exploratory coverage, not a full formal run of TC-02/TC-03 —
  specifically, the exact boundary values (€1.00, €0.99, €100.00, €100.01) and the API-level bypass
  checks (sending an invalid stake directly via `POST /api/place-bet`, skipping UI validation
  entirely) were not individually verified and documented with pass/fail evidence.
- These two are flagged as a **follow-up item**: they're good candidates to formalize either as
  additional manual test passes or, more efficiently, as parametrized automated API tests (the
  boundary matrix in TC-02 maps cleanly onto `pytest.mark.parametrize`), rather than repeating manual
  execution that largely duplicates what the automated API layer can already check deterministically.

---

## Part 1 — Top 3 Priority Scenario Execution

### TC-01 — Successful single bet placement (happy path)

**Result: FAIL**

Bet placement itself completes and a success modal is shown, but two of the expected outcomes in
the acceptance criteria are violated:
- Potential payout shown in the receipt does not match `stake × odds` (see BUG-01).
- Team order in the receipt does not match the match list order (see BUG-03).

Balance deduction itself is correct on the backend, but is not reflected live in the UI without a
manual refresh (see BUG-05).

### TC-04 — Balance is accurately deducted after a successful bet

**Result: PASS (with a related UX defect)**

Confirmed via direct before/after comparison: a single bet submission does deduct the correct stake
amount from the balance. The earlier impression that "balance stays the same" was caused by the UI
not refreshing the displayed balance live — after a manual page refresh, the correct post-bet balance
is shown. Backend deduction logic itself is correct for a single, non-duplicated submission. The
live-update gap is tracked separately as BUG-05.

### TC-05 — Duplicate/rapid Place Bet submissions are handled safely

**Result: FAIL**

Behavior is inconsistent across repeated attempts. In some runs, rapid repeated clicks on Place Bet
correctly resulted in one success and subsequent `409` responses. In other runs, multiple bets were
placed from a single burst of clicks, multiple success modals appeared, and the balance was debited
2–3x the intended stake. This is a critical, intermittent concurrency defect — see BUG-04.

---

## Part 2 — Bug Reports

### BUG-01 — Receipt "Potential Payout" does not match stake × odds

**Severity:** Critical

**Reproduction Steps:**
1. Select any match and odds (e.g. Dortmund vs Bayern Munich, odds 1.45).
2. Enter stake €10.00. Bet Slip correctly shows Potential Payout €14.50.
3. Click Place Bet.
4. Observe the Bet Receipt modal.

**Expected vs Actual:**
Expected: Potential Payout in the receipt should equal €14.50 (stake × odds), matching the value
shown in the Bet Slip before submission, per spec: *"All values should be consistent with what was
shown before placement."*
Actual: Receipt shows €20.00 — a different value than both the Bet Slip calculation and the actual
odds/stake combination. Reproduced on a second bet as well, with a different mismatched value.

**Business Impact:** Users are shown an incorrect payout figure at the exact moment they're
confirming a financial transaction. This is a direct trust and potential legal/compliance issue for
a betting product — the amount a user believes they'll win does not match what they actually agreed
to.

**Evidence:** Screenshots 1 and 2 — bet slip showing €10 @ 1.45 = correct €14.50 pre-submission, receipt
modal showing €20.00 post-submission.

---

### BUG-02 — `POST /api/reset-balance` does not restore the documented initial balance

**Severity:** High

**Reproduction Steps:**
1. Call `POST /api/reset-balance` (or trigger via any reset action in the app).
2. Call `GET /api/balance` immediately after.

**Expected vs Actual:**
Expected: Balance resets to €125.50, per spec: *"Balance — ... Starts at €125.50"* and *"Response
body and persisted state must be consistent after reset."*
Actual: Balance resets to €120.00, consistently, across multiple reset attempts.

**Business Impact:** Violates an explicitly documented contract for a QA/test-support endpoint,
undermining the reliability of any test data setup or teardown built on top of it — including this
very automation suite. If this endpoint is used in production for account correction/support
scenarios, the wrong balance is applied to the user's account.

**Evidence:** Manual verification — balance checked immediately after multiple independent reset
calls, consistently returning €120.00 instead of €125.50.

---

### BUG-03 — Team order swapped between match list and bet receipt

**Severity:** High

**Reproduction Steps:**
1. In the match list, note a match displayed as "Manchester Utd vs Chelsea" (home team first).
2. Select the Home (1) odds and place a bet.
3. Observe the Match field in the Bet Receipt modal.

**Expected vs Actual:**
Expected: Receipt shows "Manchester Utd vs Chelsea" (home team first), per spec: *"the 'home' team
is always listed first ... This convention carries through to the bet receipt."*
Actual: Receipt shows "Chelsea vs Manchester Utd" — home/away order reversed.

**Business Impact:** In combination with BUG-01, this compounds ambiguity about exactly what a user
bet on. Team order swap could cause a user to misidentify their own bet when reviewing it, which is
a meaningful trust and dispute-risk issue in a betting context.

**Evidence:** Screenshots 1 and 2 — match list entry "Manchester Utd vs Chelsea", receipt modal showing
"Chelsea vs Manchester Utd" for the same selection.

---

### BUG-04 — Rapid repeated Place Bet clicks can cause duplicate charges (race condition)

**Severity:** Critical

**Reproduction Steps:**
1. Select a match/odds and enter a valid stake.
2. Click Place Bet several times in rapid succession.
3. Repeat several times across separate attempts.

**Expected vs Actual:**
Expected, per spec: *"After submit, the UI must show an in-progress state and resolve to one final
outcome (success or failure)"*; API docs define `409` for *"bet already in progress for this user."*
Actual: Behavior is intermittent. On some attempts, only one bet is placed and subsequent clicks
correctly receive `409`. On other attempts, multiple bets are placed from one burst of rapid clicks,
multiple success modals are shown, and the balance is debited multiple times for what the user
experienced as a single action.

**Business Impact:** Direct, uncontrolled financial loss for the user (and financial/regulatory
exposure for the business) from a single accidental double-click — no client or server-side
safeguard reliably prevents it. This is the highest-severity defect found in this assessment.

**Evidence:** Manual reproduction across multiple attempts — balance decreased by 2–3x intended
stake on affected runs; multiple receipt modals observed stacking/appearing in sequence.

---

### BUG-05 — Balance does not update live in the UI after a bet is placed

**Severity:** Medium

**Reproduction Steps:**
1. Note balance shown in the header.
2. Place a single bet.
3. Without refreshing, observe the header balance.
4. Refresh the page and observe the header balance again.

**Expected vs Actual:**
Expected: Balance is decreased by the stake amount immediately after a successful bet, consistent
with the "Balance ... decreases by the stake amount when a bet is placed" business rule (this is a
UI responsiveness expectation implied by the spec's real-time framing of the balance/bet slip).
Actual: Backend balance is correctly updated (confirmed via TC-04), but the header/Bet Slip balance
in the UI remains stale until the page is manually refreshed.

**Business Impact:** Directly enables/masks BUG-04 — because the displayed balance doesn't reflect
reality, a user (or an automated/scripted actor) can continue placing bets against a balance that no
longer actually exists, increasing the risk and impact of the double-charge defect.

**Evidence:** Manual verification — balance value compared before bet, immediately after (no
refresh), and after refresh; only the post-refresh value was correct.

---

### BUG-06 — `POST /api/place-bet` response returns currency as USD instead of EUR

**Severity:** Medium

**Reproduction Steps:**
1. Call `POST /api/place-bet` with a valid payload.
2. Inspect the `currency` field in the response body.

**Expected vs Actual:**
Expected: `currency: "EUR"`, per Swagger schema (`PlaceBetResponse.currency`, example `"EUR"`) and
spec (*"Currency EUR (€)"*).
Actual: Response returns `"USD"`.

**Business Impact:** Contract violation between documented API and actual behavior; any downstream
consumer of this API (mobile app, partner integration, accounting reconciliation) relying on the
documented schema would silently misrepresent currency, with direct financial-reporting risk.

**Evidence:** Raw API response body inspected directly, `currency` field value confirmed as `"USD"`.

---

### BUG-07 — Matches with a past kickoff date are displayed and remain bettable

**Severity:** High

**Reproduction Steps:**
1. Load the match list.
2. Observe matches labeled "PAST".
3. Select odds on a "PAST" match and attempt to place a bet.

**Expected vs Actual:**
Expected: Only upcoming/pre-match events should be listed and available for betting, per spec:
*"Display upcoming football matches"* and *"Event Type: Upcoming/Pre-match events only"* (live
betting and past events are explicitly out of scope).
Actual: Matches marked "PAST" are shown in the list, and betting on them is not blocked by the UI or
API.

**Business Impact:** Allows betting on events whose outcome may already be known/determined —
a severe business-logic and potential fraud/integrity risk for a betting platform, well beyond a
cosmetic issue.

**Evidence:** Screenshot 3 of match list showing multiple entries labeled "PAST" with active, clickable
odds buttons.

---

### BUG-08 — Odds filter range (1.00–10.00) does not match documented business rule range (1.01–1000.00)

**Severity:** Medium

**Reproduction Steps:**
1. Open the Odds filter control.
2. Observe the min/max range offered.

**Expected vs Actual:**
Expected: Odds range should align with documented business rules — *"Minimum odds 1.01 / Maximum
odds 1000.00."*
Actual: Filter control offers a 1.00–10.00 range, inconsistent with the documented business rule
boundaries.

**Business Impact:** Lower severity than the financial-integrity bugs above, but limits users from
filtering to legitimately available high-odds matches (any match with odds above 10.00 becomes
unfilterable), and reflects a broader pattern of UI controls not being synced with backend business
rules.

**Evidence:** Filter control screenshot 4 showing 1.00 / 10.00 as configured min/max bounds.

---

### BUG-09 — Kickoff time is not displayed, only the date

**Severity:** Low

**Reproduction Steps:** Load the match list and inspect any match card.

**Expected vs Actual:** Expected a date/time label per spec (*"kickoff date/time label"*). Actual:
only the date is shown (e.g. "пт, 27 февр."), with no time component.

**Business Impact:** Minor UX gap — users cannot tell what time a match starts without leaving the
app, which matters for planning bets around kickoff.

**Evidence:** Match list screenshot 3, date-only label visible on each match card.

---

### BUG-10 — Available balance is not shown inside the Bet Slip

**Severity:** Low

**Reproduction Steps:** Select a match/odds to open the Bet Slip and inspect its contents.

**Expected vs Actual:** Expected per spec: *"Shows entered stake, available balance, and computed
potential payout."* Actual: available balance is shown in the page header but not repeated inside
the Bet Slip itself.

**Business Impact:** Minor UX gap; balance is still visible elsewhere on the same screen, so impact
is limited to convenience/spec compliance rather than functional risk.

**Evidence:** Bet Slip screenshot 1 — Stake and Potential Payout fields visible, no balance field
present.

---

### BUG-11 — Match list is not sorted chronologically by kickoff date

**Severity:** Low

**Reproduction Steps:** Load the match list and scroll through kickoff dates in order.

**Expected vs Actual:** Expected a chronological, predictable ordering (implied by "upcoming
matches" framing, though not explicitly specified). Actual: dates are interleaved out of order
(e.g. February entries, then March, then February again).

**Business Impact:** Low direct risk, but degrades usability/trust — users scanning for the soonest
match to bet on cannot rely on visual order.

**Evidence:** Match list screenshot 5 showing non-chronological date sequence across visible entries.

---

## Summary

| ID | Title | Severity |
|----|-------|----------|
| BUG-01 | Receipt payout doesn't match stake × odds | Critical |
| BUG-04 | Rapid clicks can duplicate charges (race condition) | Critical |
| BUG-02 | Reset-balance restores wrong value | High |
| BUG-03 | Team order swapped in receipt | High |
| BUG-07 | PAST matches shown and bettable | High |
| BUG-05 | Balance doesn't update live in UI | Medium |
| BUG-06 | place-bet API returns USD instead of EUR | Medium |
| BUG-08 | Odds filter range mismatched with business rules | Medium |
| BUG-09 | Kickoff time not shown | Low |
| BUG-10 | Available balance not shown in Bet Slip | Low |
| BUG-11 | Match list not sorted by date | Low |
