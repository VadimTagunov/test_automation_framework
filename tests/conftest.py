"""Root-level fixtures shared across the UI and API test suites."""
import pytest

from api.balance_client import BalanceClient
from config.config import Config


@pytest.fixture
def config() -> type[Config]:
    return Config


@pytest.fixture(autouse=True)
def reset_balance() -> None:
    """Reset the test account's balance before every test.

    Keeps stake-dependent tests deterministic regardless of run order or
    how much balance prior runs have consumed. Note: due to a known
    application defect, this endpoint persists a balance of 120.00 rather
    than the documented 125.50 -- either way it leaves enough headroom for
    this suite's stakes.
    """
    BalanceClient(Config.API_BASE_URL, Config.USER_ID, Config.DEFAULT_TIMEOUT).reset_balance()
