"""Thread-safe registry for the active WebDriver.

Element does not receive a driver explicitly when created -- it fetches it
from here. The registry is built on threading.local, so when tests run in
parallel across multiple threads, each thread only ever sees its own
driver, not a neighboring test's.
"""
from __future__ import annotations

import threading

from selenium.webdriver.remote.webdriver import WebDriver


class DriverManager:
    _storage = threading.local()

    @classmethod
    def set_driver(cls, driver: WebDriver) -> None:
        cls._storage.driver = driver

    @classmethod
    def get_driver(cls) -> WebDriver:
        driver = getattr(cls._storage, "driver", None)
        if driver is None:
            raise RuntimeError(
                "No WebDriver registered for the current thread. "
                "Call DriverManager.set_driver() before using page elements."
            )
        return driver

    @classmethod
    def clear_driver(cls) -> None:
        cls._storage.driver = None
