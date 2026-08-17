"""Shared HTTP request logic for all API clients."""
from __future__ import annotations

import json
from typing import Any

import allure
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

    def _request(self, method: str, path: str, **kwargs: Any) -> requests.Response:
        url = self._url(path)
        request_body = kwargs.get("json")

        with allure.step(f"Request: {method} {url}"):
            if request_body is not None:
                allure.attach(
                    json.dumps(request_body),
                    name="Request body",
                    attachment_type=allure.attachment_type.JSON,
                )
            response = self.session.request(method, url, timeout=self.timeout, **kwargs)

        with allure.step(f"Response: {response.status_code}"):
            allure.attach(
                response.text,
                name="Response body",
                attachment_type=allure.attachment_type.JSON,
            )

        return response

    def get(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, json: dict | None = None, **kwargs: Any) -> requests.Response:
        return self._request("POST", path, json=json, **kwargs)

    def put(self, path: str, json: dict | None = None, **kwargs: Any) -> requests.Response:
        return self._request("PUT", path, json=json, **kwargs)

    def delete(self, path: str, **kwargs: Any) -> requests.Response:
        return self._request("DELETE", path, **kwargs)
