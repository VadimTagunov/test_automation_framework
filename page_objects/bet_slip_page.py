"""Пейдж-обджект панели ставки (ввод суммы и отправка ставки)."""
import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from page_objects.base_page import BasePage
from page_objects.element import Element


class BetSlipPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.stake_input = Element(By.ID, "bet-slip-stake-input")
        self.place_bet_button = Element(By.ID, "bet-slip-place-bet")
        self.total_stake = Element(By.ID, "bet-slip-total-stake")
        self.potential_payout = Element(By.ID, "bet-slip-potential-payout")
        self.remove_selection_button = Element(By.ID, "bet-slip-selection-remove")

    @allure.step("Ввести ставку {stake}")
    def enter_stake(self, stake: str) -> None:
        self.stake_input.type(stake)

    @allure.step("Нажать кнопку Place Bet")
    def click_place_bet(self) -> None:
        self.place_bet_button.click()

    @allure.step("Получить потенциальную выплату из бет-слипа")
    def get_potential_payout_text(self) -> str:
        return self.potential_payout.get_text()
