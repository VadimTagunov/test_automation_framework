import allure
import requests

from src.api.base.base_client import BaseClient


class MatchesClient(BaseClient):
    """Client for the /api/matches resource."""

    @allure.step("Get all matches")
    def get_matches(self) -> requests.Response:
        return self.get("/api/matches")
