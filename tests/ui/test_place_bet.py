"""UI E2E coverage for the core bet-placement journey."""
import re

import allure
import pytest

from src.ui.app.app import App

VALID_STAKE = 10.00
BET_ID_PATTERN = re.compile(r"^#B-\d+$")


@allure.severity(allure.severity_level.BLOCKER)
@allure.title("Place a single bet and verify the success receipt")
@pytest.mark.ui
def test_successful_single_bet_placement(app: App) -> None:
    """Successful single bet placement.

    Selecting a match, picking an outcome, staking money and receiving a
    confirmation is the core revenue-generating journey of a sports betting
    app: if a user cannot complete it, the product generates no revenue at
    all. That makes it the single highest-value candidate for UI
    automation, ahead of secondary flows like filtering or formatting.

    Where the known payout-mismatch and team-order-swap defects would
    affect an assertion, this test still asserts the spec-correct expected
    value rather than working around the bug. It documents real product
    behavior and is expected to fail on those assertions while the
    underlying defects remain in the application.
    """
    with allure.step("Read the first upcoming match and its HOME odds"):
        match = app.match_list.get_first_match()
        odds = app.match_list.get_odds_value(match.match_id, "HOME")

    with allure.step("Select the HOME outcome for that match"):
        app.match_list.select_outcome(match.match_id, "HOME")

    with allure.step(f"Enter a valid stake of {VALID_STAKE:.2f}"):
        app.bet_slip.enter_stake(f"{VALID_STAKE:.2f}")

    with allure.step("Submit the bet"):
        app.bet_slip.click_place_bet()

    with allure.step("Verify the success receipt appears with expected fields"):
        app.receipt_modal.wait_until_visible()
        bet_id = app.receipt_modal.get_bet_id()
        assert BET_ID_PATTERN.match(bet_id), f"Expected a Bet ID like '#B-12345', got {bet_id!r}"
        assert app.receipt_modal.get_stake_text() == f"€{VALID_STAKE:.2f}"
        assert app.receipt_modal.get_odds_text() == f"{odds:.2f}"

    with allure.step("Verify the match label matches home/away order shown pre-submission"):
        # Known defect: home/away order is sometimes reversed on the receipt.
        # Asserting the spec-correct order on purpose (see docstring).
        expected_match_label = f"{match.home_team} vs {match.away_team}"
        assert app.receipt_modal.get_match_label() == expected_match_label

    with allure.step("Verify potential payout equals stake x odds shown pre-submission"):
        # Known defect: receipt payout does not always equal stake x odds.
        # Asserting the spec-correct value on purpose (see docstring).
        expected_payout = VALID_STAKE * odds
        assert app.receipt_modal.get_payout_text() == f"€{expected_payout:.2f}"
