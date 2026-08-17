"""Shared HTTP request logic for all API clients."""
from __future__ import annotations

from typing import Any

import requests


class BaseClient:
    """Holds a requests.Session with base URL and auth header wiring.

    Endpoint-specific clients (MatchesClient, BalanceClient, BetsClient)
    subclass this and add methods for their own resource only.
    """

    def __init__(self, base_url: str, user_id: str, timeout: float = 15.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update(
            {
                "x-user-id": user_id,
                "Content-Type": "application/json",
                "Accept": "application/json",
            }
        )

    def _url(self, path: str) -> str:
        return f"{self.base_url}/{path.lstrip('/')}"

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self.session.get(self._url(path), timeout=self.timeout, **kwargs)

    def post(self, path: str, json: dict | None = None, **kwargs: Any) -> requests.Response:
        return self.session.post(self._url(path), json=json, timeout=self.timeout, **kwargs)

    def put(self, path: str, json: dict | None = None, **kwargs: Any) -> requests.Response:
        return self.session.put(self._url(path), json=json, timeout=self.timeout, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self.session.delete(self._url(path), timeout=self.timeout, **kwargs)
