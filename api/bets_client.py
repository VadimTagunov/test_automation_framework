import requests

from api.base_client import BaseClient


class BetsClient(BaseClient):
    """Client for the /api/place-bet resource."""

    def place_bet(self, match_id: str, selection: str, stake: float) -> requests.Response:
        return self.post(
            "/api/place-bet",
            json={"matchId": match_id, "selection": selection, "stake": stake},
        )
