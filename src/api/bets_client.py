import allure
import requests

from src.api.base.base_client import BaseClient


class BetsClient(BaseClient):
    """Client for the /api/place-bet resource."""

    @allure.step("Place a bet: match {match_id}, selection {selection}, stake {stake}")
    def place_bet(self, match_id: str, selection: str, stake: float) -> requests.Response:
        return self.post(
            "/api/place-bet",
            json={"matchId": match_id, "selection": selection, "stake": stake},
        )
