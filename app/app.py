"""App entity: instantiates and exposes all page objects together."""
from selenium.webdriver.remote.webdriver import WebDriver

from src.page_object.bet_slip_page import BetSlipPage
from src.page_object.match_list_page import MatchListPage
from src.page_object.receipt_modal import ReceiptModal


class App:
    def __init__(self, driver: WebDriver) -> None:
        self.driver = driver
        self.match_list = MatchListPage(driver)
        self.bet_slip = BetSlipPage(driver)
        self.receipt_modal = ReceiptModal(driver)
