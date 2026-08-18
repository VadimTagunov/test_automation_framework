import requests

from src.api.base.base_client import BaseClient
from src.support.step import step


class MatchesClient(BaseClient):
    """Client for the /api/matches resource."""

    @step("Get all matches")
    def get_matches(self) -> requests.Response:
        return self.get("/api/matches")
