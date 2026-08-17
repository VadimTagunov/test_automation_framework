"""UI-only fixtures: webdriver lifecycle and the `app` fixture."""
from collections.abc import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from app.app import App
from config.config import Config


@pytest.fixture
def driver() -> Generator[WebDriver, None, None]:
    """Chrome driver via Selenium Manager (built into Selenium 4.6+)."""
    options = Options()
    if Config.HEADLESS:
        options.add_argument("--headless=new")
    options.add_argument(f"--window-size={Config.WINDOW_SIZE}")
    options.add_argument("--disable-gpu")

    chrome_driver = webdriver.Chrome(options=options)
    chrome_driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
    yield chrome_driver
    chrome_driver.quit()


@pytest.fixture
def app(driver: WebDriver) -> Generator[App, None, None]:
    """Navigate to the app (with the required user-id param) and build App."""
    driver.get(Config.ui_url())
    application = App(driver)
    application.match_list.wait_for_matches_to_load()
    yield application
