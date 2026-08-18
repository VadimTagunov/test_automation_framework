import requests

from src.api.base.base_client import BaseClient
from src.support.step import step


class BalanceClient(BaseClient):
    """Client for the /api/balance and /api/reset-balance resources."""

    @step("Get balance")
    def get_balance(self) -> requests.Response:
        return self.get("/api/balance")

    @step("Reset balance")
    def reset_balance(self) -> requests.Response:
        return self.post("/api/reset-balance")
