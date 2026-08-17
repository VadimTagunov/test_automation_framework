"""Wrapper around a web element.

Holds only the search strategy (id, css, xpath, ...) and the locator value
-- the driver is not passed into the constructor, it is lazily fetched from
DriverManager on every interaction. Encapsulates all element interaction
logic: click, type text, read text and attributes, visibility waits. The
element is re-located on every call rather than cached, to avoid
StaleElementReference after React re-renders.
"""
from __future__ import annotations

from selenium.common.exceptions import TimeoutException
from selenium.webdriver.remote.webelement import WebElement as SeleniumWebElement
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from config.config import Config
from driver.manager import DriverManager


class Element:
    def __init__(self, by: str, locator: str) -> None:
        self.by = by
        self.locator = locator

    @property
    def _by_locator(self) -> tuple[str, str]:
        return self.by, self.locator

    @property
    def _wait(self) -> WebDriverWait:
        return WebDriverWait(DriverManager.get_driver(), Config.DEFAULT_TIMEOUT)

    def find(self) -> SeleniumWebElement:
        return self._wait.until(EC.presence_of_element_located(self._by_locator))

    def find_visible(self) -> SeleniumWebElement:
        return self._wait.until(EC.visibility_of_element_located(self._by_locator))

    def find_all(self) -> list[SeleniumWebElement]:
        return self._wait.until(EC.presence_of_all_elements_located(self._by_locator))

    def click(self) -> None:
        self._wait.until(EC.element_to_be_clickable(self._by_locator)).click()

    def type(self, text: str) -> None:
        field = self.find_visible()
        field.clear()
        field.send_keys(text)

    def get_text(self) -> str:
        return self.find().text

    def get_attribute(self, name: str) -> str | None:
        return self.find().get_attribute(name)

    def is_displayed(self) -> bool:
        try:
            return self.find_visible().is_displayed()
        except TimeoutException:
            return False

    def wait_until_visible(self) -> None:
        self._wait.until(EC.visibility_of_element_located(self._by_locator))

    def wait_until_invisible(self) -> None:
        self._wait.until(EC.invisibility_of_element_located(self._by_locator))
