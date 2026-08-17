"""Page object for the post-bet success receipt modal."""
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from page_objects.base_page import BasePage


class ReceiptModal(BasePage):
    ROOT = (By.ID, "modal-success")
    BET_ID = (By.ID, "modal-success-bet-id")
    MATCH_LABEL = (By.ID, "modal-success-match")
    STAKE = (By.ID, "modal-success-stake")
    ODDS = (By.ID, "modal-success-odds")
    PAYOUT = (By.ID, "modal-success-payout")
    CLOSE_BUTTON = (By.ID, "modal-success-close")

    def wait_until_visible(self) -> None:
        self.wait.until(EC.visibility_of_element_located(self.ROOT))

    def get_bet_id(self) -> str:
        return self.text_of(self.BET_ID)

    def get_match_label(self) -> str:
        return self.text_of(self.MATCH_LABEL)

    def get_stake_text(self) -> str:
        return self.text_of(self.STAKE)

    def get_odds_text(self) -> str:
        return self.text_of(self.ODDS)

    def get_payout_text(self) -> str:
        return self.text_of(self.PAYOUT)

    def close(self) -> None:
        self.click(self.CLOSE_BUTTON)
