"""Потокобезопасное хранилище активного WebDriver.

Element не получает driver явно при создании -- он берёт его отсюда. Хранилище
построено на threading.local, поэтому при параллельном запуске тестов в
разных потоках каждый поток видит только свой собственный драйвер, а не
драйвер соседнего теста.
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
