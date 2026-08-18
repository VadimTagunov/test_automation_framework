"""Shared infrastructure for page objects."""
from selenium.webdriver.remote.webdriver import WebDriver


class BasePage:
    """Base class for page objects and their components.

    Each page object takes a driver in its constructor and describes
    elements and behavior for its own page/component only -- no
    cross-page logic. Pages don't normally need the driver directly
    (elements get it through DriverManager), but it's kept here in case a
    specific page needs a driver-level action (navigation, JS, switching
    windows, etc.).
    """

    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
