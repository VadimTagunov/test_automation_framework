"""Page object for the upcoming-matches list."""
from dataclasses import dataclass

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from page_objects.base_page import BasePage


@dataclass(frozen=True)
class MatchSummary:
    match_id: str
    home_team: str
    away_team: str


class MatchListPage(BasePage):
    LOADING_SPINNER = (By.ID, "match-list-loading")
    MATCH_CARDS = (By.CSS_SELECTOR, ".matchCard")

    def wait_for_matches_to_load(self) -> None:
        self.wait.until(EC.invisibility_of_element_located(self.LOADING_SPINNER))
        self.wait.until(EC.presence_of_element_located(self.MATCH_CARDS))

    def get_first_match(self) -> MatchSummary:
        card = self.find_all(self.MATCH_CARDS)[0]
        match_id = card.get_attribute("id").removeprefix("match-card-")
        team_names = card.find_elements(By.CSS_SELECTOR, ".teamName")
        return MatchSummary(
            match_id=match_id,
            home_team=team_names[0].text,
            away_team=team_names[1].text,
        )

    def get_odds_value(self, match_id: str, selection: str) -> float:
        locator = (By.CSS_SELECTOR, f"#odds-{match_id}-{selection.lower()} .oddsButtonValue")
        return float(self.find(locator).text)

    def select_outcome(self, match_id: str, selection: str) -> None:
        self.click((By.ID, f"odds-{match_id}-{selection.lower()}"))
