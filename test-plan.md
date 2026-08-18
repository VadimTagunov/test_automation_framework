# Test Plan — Single Bet Placement

**Application under test:** https://qae-assignment-tau.vercel.app/
**Feature:** Single Bet Placement (Sports Betting QA Assessment App)
**Scope:** UI + API, desktop Chrome
**Reference:** Single Bet Placement Feature Specification, Swagger/OpenAPI docs (`/api/docs?format=json`)

## Scenario Selection Rationale

This set of 6 scenarios was chosen to give range across the risk surface of the feature rather than
exhaustive coverage: one happy path (core revenue flow), two negative/validation cases around the
highest-risk input (stake), and three scenarios that specifically target **data and financial
integrity** — balance deduction, concurrent submissions, and receipt consistency. These three were
prioritized because a betting product's core trust contract is "the numbers are always right and
money is never lost/duplicated." Exploratory testing during reconnaissance surfaced concrete evidence
that this contract is currently broken in several places, which directly informed prioritization below.

---

## TC-01 — Successful single bet placement (happy path)

**Priority:** Critical

**Risk Rationale:** This is the core revenue-generating user journey. Any regression here blocks the
entire feature. It's also the baseline all other scenarios are compared against.

**Steps:**
1. Navigate to the app with a valid `user-id`.
2. Select an upcoming match from the match list.
3. Click one of the three odds buttons (e.g. `1` — Home).
4. Enter a valid stake within limits (e.g. €10.00).
5. Note the potential payout shown in the Bet Slip before submitting.
6. Click **Place Bet**.
7. Observe the loading state, then the resulting modal.

**Expected Result:**
- Button shows a `Placing...` in-progress state, then resolves to exactly one final outcome.
- Success modal (Bet Receipt) appears showing: Bet ID, match (home team listed first, matching the
  match list order), selection, stake, odds, potential payout, and timestamp.
- Potential payout in the receipt equals `stake × odds` and matches the value shown in the Bet Slip
  pre-submission.
- Balance is decreased by the stake amount and reflects correctly without requiring a manual refresh.

---

## TC-02 — Stake validation: boundaries and precision

**Priority:** High

**Risk Rationale:** Stake is the single highest-risk input field — it directly maps to real money.
Boundary and precision handling here has both financial and compliance implications (accepting
invalid stakes could allow exploitation; rejecting valid ones blocks legitimate revenue).

**Steps (run as a data set against the same selected match):**
1. Attempt to place a bet with stake = €0.
2. Attempt to place a bet with stake = €0.99 (just below minimum).
3. Attempt to place a bet with stake = €1.00 (minimum boundary).
4. Attempt to place a bet with stake = €100.00 (maximum boundary).
5. Attempt to place a bet with stake = €100.01 (just above maximum).
6. Attempt to place a bet with stake = €10.005 (3 decimal places).
7. Attempt to place a bet with a non-numeric stake (e.g. `abc`), via API directly (bypassing UI input
   masking).

**Expected Result:**
- €0, €0.99, €100.01, and 3-decimal stakes are rejected by the UI (Place Bet disabled/blocked) and,
  if sent directly via API, rejected with `422` and the corresponding error code
  (`invalid_stake_min` / `invalid_stake_max` / `invalid_stake_precision`).
- €1.00 and €100.00 are accepted (inclusive boundaries).
- Non-numeric stake via API returns `422 invalid_stake_type`.
- Error messaging matches the documented copy ("Minimum stake is €1.00", "Maximum stake is €100.00").

**Note:** Live testing found the documented minimum stake is inconsistent between the PDF spec's
Business Rules section (€1.00) and its Validation Rules section (€1.01). The Swagger contract and
live API error message confirm **€1.00** as the authoritative minimum — this test plan follows the
verified API contract.

---

## TC-03 — Stake exceeding available balance

**Priority:** High

**Risk Rationale:** Distinct from the static min/max boundary check — this is a dynamic check against
the user's current state. If bypassed, a user could place a bet with money they don't have, which is
a direct financial-integrity risk.

**Steps:**
1. Note current available balance (e.g. €115.50).
2. Attempt to enter and submit a stake greater than the current balance but within the €1–€100 static
   range (e.g. balance is €50, stake entered is €75).
3. Repeat the same request directly via `POST /api/place-bet`, bypassing the UI.

**Expected Result:**
- UI blocks submission with an "Insufficient balance" message.
- API rejects the request (`422`, `insufficient_balance`) even when the static stake range (€1–€100)
  is otherwise satisfied.

---

## TC-04 — Balance is accurately deducted after a successful bet

**Priority:** Critical

**Risk Rationale:** Reconnaissance testing found strong indications that balance changes are
unreliable: the UI does not update balance live (only after a manual refresh), and in some cases the
balance does not appear to change at all after a single successful bet. If stake is genuinely not
deducted on the backend (not just a stale UI read), this is a critical financial-integrity defect —
users could place unlimited bets without ever being charged.

**Steps:**
1. Call `GET /api/balance` directly and record the exact value.
2. Place a single bet via `POST /api/place-bet` with a known stake (e.g. €10.00), only one submission.
3. Immediately call `GET /api/balance` again (API-level, no UI/refresh involved).
4. Separately, repeat via the UI: note balance, place one bet, refresh the page, check displayed
   balance.

**Expected Result:**
- Balance returned by the API after the bet equals `balance_before − stake`, exactly, with no
  refresh or additional action required.
- UI balance after refresh matches the API value.
- This isolates whether the defect is a stale-UI issue (balance not pushed without refresh) versus a
  genuine backend failure to persist the deduction — both are defects, but the latter is materially
  more severe and should be reported and prioritized as such.

---

## TC-05 — Duplicate/rapid Place Bet submissions are handled safely

**Priority:** Critical

**Risk Rationale:** This targets a race condition found during exploratory testing: rapidly clicking
Place Bet multiple times sometimes triggers multiple successful charges and multiple receipt modals,
instead of being blocked by the documented `409` conflict response. This is the single highest
financial-risk defect candidate in the feature — it means the same stake can be charged 2-3x for one
user action.

**Steps:**
1. Select a match and enter a valid stake.
2. Click **Place Bet** multiple times in rapid succession (simulate via fast repeated clicks and, for
   the automated version, via near-simultaneous API calls).
3. Observe the number of resulting success modals and the final balance.
4. Repeat several times to check consistency, since initial observation suggests this is intermittent.

**Expected Result:**
- Exactly one bet is placed and one success modal is shown.
- All subsequent rapid submissions while the first is in-flight receive `409` ("bet already in
  progress for this user") and are not charged.
- Balance decreases by exactly one stake amount, never more, regardless of click speed or count.

---

## TC-06 — Receipt data integrity (teams, odds, payout consistency)

**Priority:** High

**Risk Rationale:** Reconnaissance found that team order in the receipt does not always match the
match list (home/away order swapped), and that potential payout shown in the receipt can differ from
the value shown in the Bet Slip pre-submission and from `stake × odds`. In a betting product this
directly undermines user trust — the user needs certainty about exactly what they bet on and what
they stand to win, and the spec explicitly requires this consistency.

**Steps:**
1. Note the match list order (home team listed first, per spec convention) and the selection made,
   odds, and potential payout shown in the Bet Slip before submitting.
2. Submit the bet.
3. Compare the Bet Receipt modal's match order, odds, and potential payout against what was recorded
   in step 1 and against `stake × odds` calculated independently.
4. Repeat for at least 3 different matches/odds combinations to rule out a one-off rendering glitch.

**Expected Result:**
- Team order in the receipt matches the match list order (home team first) exactly.
- Odds shown in the receipt match the odds at the time of selection.
- Potential payout in the receipt equals `stake × odds` and matches the pre-submission Bet Slip value,
  with no discrepancy.
