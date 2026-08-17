import requests

from src.api.base.base_client import BaseClient


class MatchesClient(BaseClient):
    """Client for the /api/matches resource."""

    def get_matches(self) -> requests.Response:
        return self.get("/api/matches")
