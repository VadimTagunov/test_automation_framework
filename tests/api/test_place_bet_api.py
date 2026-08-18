"""API coverage for the stake business rule validation on POST /api/place-bet."""
import allure
import pytest

from src.api.bets_client import BetsClient
from src.api.matches_client import MatchesClient

BELOW_MIN_STAKE = 0.50
SELECTION = "HOME"


@allure.severity(allure.severity_level.NORMAL)
@allure.title("Reject a stake below the documented minimum")
@pytest.mark.api
def test_place_bet_rejects_stake_below_minimum(
    matches_client: MatchesClient, bets_client: BetsClient
) -> None:
    """Stake-below-minimum is rejected with 422 invalid_stake_min.

    The minimum-stake rule (>= EUR 1.00) is a pure business-rule /
    validation check: it does not depend on UI rendering or account state,
    and has exactly one deterministic expected outcome regardless of which
    match or selection is used. Verifying it directly against the API is
    faster and more reliable than driving the same rule through the UI,
    which would add browser overhead without covering the rule any better.
    """
    matches_response = matches_client.get_matches()
    assert matches_response.status_code == 200
    match_id = matches_response.json()[0]["id"]

    response = bets_client.place_bet(match_id, SELECTION, BELOW_MIN_STAKE)

    assert response.status_code == 422
    body = response.json()
    assert body["error"] == "invalid_stake_min"
