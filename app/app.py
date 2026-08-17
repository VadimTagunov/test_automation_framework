"""App entity: instantiates and exposes all page objects together."""
from selenium.webdriver.remote.webdriver import WebDriver

from page_objects.bet_slip_page import BetSlipPage
from page_objects.match_list_page import MatchListPage
from page_objects.receipt_modal import ReceiptModal


class App:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.match_list = MatchListPage(driver)
        self.bet_slip = BetSlipPage(driver)
        self.receipt_modal = ReceiptModal(driver)
