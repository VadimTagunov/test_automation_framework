"""API-only fixtures: one client per resource."""
import pytest

from src.api.balance_client import BalanceClient
from src.api.bets_client import BetsClient
from src.api.matches_client import MatchesClient
from config.config import Config


@pytest.fixture
def matches_client() -> MatchesClient:
    return MatchesClient(Config.API_BASE_URL, Config.USER_ID, Config.DEFAULT_TIMEOUT)


@pytest.fixture
def balance_client() -> BalanceClient:
    return BalanceClient(Config.API_BASE_URL, Config.USER_ID, Config.DEFAULT_TIMEOUT)


@pytest.fixture
def bets_client() -> BetsClient:
    return BetsClient(Config.API_BASE_URL, Config.USER_ID, Config.DEFAULT_TIMEOUT)
