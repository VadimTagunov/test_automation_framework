"""Page object for the bet slip panel (stake entry and submission)."""
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from src.support.step import step
from src.ui.page_object.base.base_page import BasePage
from src.ui.page_object.base.element import Element


class BetSlipPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.stake_input = Element(By.ID, "bet-slip-stake-input")
        self.place_bet_button = Element(By.ID, "bet-slip-place-bet")
        self.total_stake = Element(By.ID, "bet-slip-total-stake")
        self.potential_payout = Element(By.ID, "bet-slip-potential-payout")
        self.remove_selection_button = Element(By.ID, "bet-slip-selection-remove")

    @step("Enter stake {stake}")
    def enter_stake(self, stake: str) -> None:
        self.stake_input.type(stake)

    @step("Click the Place Bet button")
    def click_place_bet(self) -> None:
        self.place_bet_button.click()

    @step("Get the potential payout from the bet slip")
    def get_potential_payout_text(self) -> str:
        return self.potential_payout.get_text()
