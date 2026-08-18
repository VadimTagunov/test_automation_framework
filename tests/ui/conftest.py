"""UI-only fixtures: webdriver lifecycle and the `app` fixture."""
from collections.abc import Generator

import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.remote.webdriver import WebDriver

from config.config import Config
from src.support.step import step
from src.ui.app.app import App
from src.ui.driver.manager import DriverManager


@pytest.fixture
def driver() -> Generator[WebDriver, None, None]:
    """Chrome driver via Selenium Manager (built into Selenium 4.6+).

    Registers the driver in DriverManager for the current thread so that
    page-object Elements can pick it up without having it passed to them.
    """
    with step(f"Launch Chrome driver (headless={Config.HEADLESS})"):
        options = Options()
        if Config.HEADLESS:
            options.add_argument("--headless=new")
        options.add_argument(f"--window-size={Config.WINDOW_SIZE}")
        options.add_argument("--disable-gpu")

        chrome_driver = webdriver.Chrome(options=options)
        chrome_driver.set_page_load_timeout(Config.PAGE_LOAD_TIMEOUT)
        DriverManager.set_driver(chrome_driver)

    yield chrome_driver

    with step("Shut down the Chrome driver"):
        DriverManager.clear_driver()
        chrome_driver.quit()


@pytest.fixture
def app(driver: WebDriver) -> Generator[App, None, None]:
    """Navigate to the app (with the required user-id param) and build App."""
    with step(f"Open the app at {Config.ui_url()}"):
        driver.get(Config.ui_url())
        application = App(driver)
        application.match_list.wait_for_matches_to_load()

    yield application
