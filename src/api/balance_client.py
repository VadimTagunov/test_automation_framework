import allure
import requests

from src.api.base.base_client import BaseClient


class BalanceClient(BaseClient):
    """Client for the /api/balance and /api/reset-balance resources."""

    @allure.step("Get balance")
    def get_balance(self) -> requests.Response:
        return self.get("/api/balance")

    @allure.step("Reset balance")
    def reset_balance(self) -> requests.Response:
        return self.post("/api/reset-balance")
