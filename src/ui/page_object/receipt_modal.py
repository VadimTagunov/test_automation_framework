"""Page object for the post-bet success receipt modal."""
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.ui.page_object.base.base_page import BasePage
from src.ui.page_object.base.element import Element


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

    @allure.step("Wait for the success receipt modal to appear")
    def wait_until_visible(self) -> None:
        self.root.wait_until_visible()

    @allure.step("Get the bet id from the receipt")
    def get_bet_id(self) -> str:
        return self.bet_id.get_text()

    @allure.step("Get the match label from the receipt")
    def get_match_label(self) -> str:
        return self.match_label.get_text()

    @allure.step("Get the stake amount from the receipt")
    def get_stake_text(self) -> str:
        return self.stake.get_text()

    @allure.step("Get the odds from the receipt")
    def get_odds_text(self) -> str:
        return self.odds.get_text()

    @allure.step("Get the potential payout from the receipt")
    def get_payout_text(self) -> str:
        return self.payout.get_text()

    @allure.step("Close the receipt modal")
    def close(self) -> None:
        self.close_button.click()
