import requests

from api.base_client import BaseClient


class BalanceClient(BaseClient):
    """Client for the /api/balance and /api/reset-balance resources."""

    def get_balance(self) -> requests.Response:
        return self.get("/api/balance")

    def reset_balance(self) -> requests.Response:
        return self.post("/api/reset-balance")
