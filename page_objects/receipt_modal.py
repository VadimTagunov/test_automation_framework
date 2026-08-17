"""Пейдж-обджект модального окна с чеком после успешной ставки."""
import allure
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

    @allure.step("Дождаться появления модального окна с чеком")
    def wait_until_visible(self) -> None:
        self.root.wait_until_visible()

    @allure.step("Получить ID ставки из чека")
    def get_bet_id(self) -> str:
        return self.bet_id.get_text()

    @allure.step("Получить название матча из чека")
    def get_match_label(self) -> str:
        return self.match_label.get_text()

    @allure.step("Получить сумму ставки из чека")
    def get_stake_text(self) -> str:
        return self.stake.get_text()

    @allure.step("Получить коэффициент из чека")
    def get_odds_text(self) -> str:
        return self.odds.get_text()

    @allure.step("Получить потенциальную выплату из чека")
    def get_payout_text(self) -> str:
        return self.payout.get_text()

    @allure.step("Закрыть модальное окно с чеком")
    def close(self) -> None:
        self.close_button.click()
