"""Page object for the bet slip panel (stake entry and submission)."""
from selenium.webdriver.common.by import By

from page_objects.base_page import BasePage


class BetSlipPage(BasePage):
    STAKE_INPUT = (By.ID, "bet-slip-stake-input")
    PLACE_BET_BUTTON = (By.ID, "bet-slip-place-bet")
    TOTAL_STAKE = (By.ID, "bet-slip-total-stake")
    POTENTIAL_PAYOUT = (By.ID, "bet-slip-potential-payout")
    REMOVE_SELECTION_BUTTON = (By.ID, "bet-slip-selection-remove")

    def enter_stake(self, stake: str) -> None:
        field = self.find_visible(self.STAKE_INPUT)
        field.clear()
        field.send_keys(stake)

    def click_place_bet(self) -> None:
        self.click(self.PLACE_BET_BUTTON)

    def get_potential_payout_text(self) -> str:
        return self.text_of(self.POTENTIAL_PAYOUT)
