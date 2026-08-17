"""Central configuration for the test automation framework.

Values are read from environment variables where set, falling back to the
defaults for this assignment's environment. This is a plain class (not a
fixture) so it can be imported directly from anywhere -- tests, page
objects, or API clients -- without going through pytest's dependency
injection.
"""
from __future__ import annotations

import os


class Config:
    BASE_URL: str = os.getenv("BASE_URL", "https://qae-assignment-tau.vercel.app")
    API_BASE_URL: str = os.getenv("API_BASE_URL", BASE_URL)
    USER_ID: str = os.getenv("USER_ID", "candidate-7PeYkDh0CI")

    DEFAULT_TIMEOUT: float = float(os.getenv("DEFAULT_TIMEOUT", "15"))
    PAGE_LOAD_TIMEOUT: float = float(os.getenv("PAGE_LOAD_TIMEOUT", "30"))

    HEADLESS: bool = os.getenv("HEADLESS", "true").lower() in ("1", "true", "yes")
    WINDOW_SIZE: str = os.getenv("WINDOW_SIZE", "1440,900")

    # Business rules from the API spec (used by API-level tests).
    MIN_STAKE: float = 1.00
    MAX_STAKE: float = 100.00
    CURRENCY: str = "EUR"

    @classmethod
    def ui_url(cls, user_id: str | None = None) -> str:
        """Base URL with the required user-id query param appended."""
        return f"{cls.BASE_URL}/?user-id={user_id or cls.USER_ID}"
