"""Пейдж-обджект модального окна с чеком после успешной ставки."""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from page_objects.base_page import BasePage
from page_objects.element import Element


class ReceiptModal(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.root = Element(By.ID, "modal-success")
        self.bet_id = Element(By.ID, "modal-success-bet-id")
        self.match_label = Element(By.ID, "modal-success-match")
        self.stake = Element(By.ID, "modal-success-stake")
        self.odds = Element(By.ID, "modal-success-odds")
        self.payout = Element(By.ID, "modal-success-payout")
        self.close_button = Element(By.ID, "modal-success-close")

    def wait_until_visible(self) -> None:
        self.root.wait_until_visible()

    def get_bet_id(self) -> str:
        return self.bet_id.get_text()

    def get_match_label(self) -> str:
        return self.match_label.get_text()

    def get_stake_text(self) -> str:
        return self.stake.get_text()

    def get_odds_text(self) -> str:
        return self.odds.get_text()

    def get_payout_text(self) -> str:
        return self.payout.get_text()

    def close(self) -> None:
        self.close_button.click()
