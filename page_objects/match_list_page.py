"""Page object for the upcoming matches list."""
from dataclasses import dataclass

import allure
from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webdriver import WebDriver

from page_objects.base_page import BasePage
from page_objects.element import Element


@dataclass(frozen=True)
class MatchSummary:
    match_id: str
    home_team: str
    away_team: str


class MatchListPage(BasePage):
    def __init__(self, driver: WebDriver) -> None:
        super().__init__(driver)
        self.loading_spinner = Element(By.ID, "match-list-loading")
        self.match_cards = Element(By.CSS_SELECTOR, ".matchCard")

    @allure.step("Wait for the match list to load")
    def wait_for_matches_to_load(self) -> None:
        self.loading_spinner.wait_until_invisible()
        self.match_cards.find()

    @allure.step("Get the first match from the list")
    def get_first_match(self) -> MatchSummary:
        card = self.match_cards.find_all()[0]
        match_id = card.get_attribute("id").removeprefix("match-card-")
        team_names = card.find_elements(By.CSS_SELECTOR, ".teamName")
        return MatchSummary(
            match_id=match_id,
            home_team=team_names[0].text,
            away_team=team_names[1].text,
        )

    @allure.step("Get the {selection} odds value for match {match_id}")
    def get_odds_value(self, match_id: str, selection: str) -> float:
        odds_value = Element(
            By.CSS_SELECTOR, f"#odds-{match_id}-{selection.lower()} .oddsButtonValue"
        )
        return float(odds_value.get_text())

    @allure.step("Select the {selection} outcome for match {match_id}")
    def select_outcome(self, match_id: str, selection: str) -> None:
        outcome_button = Element(By.ID, f"odds-{match_id}-{selection.lower()}")
        outcome_button.click()
