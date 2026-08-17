# test_automation_framework

Test automation for the Sports Betting QA assignment app: UI (Selenium) and API (requests) coverage for `pytest`.

## Prerequisites

- Python 3.9+
- Google Chrome installed locally (the UI suite drives Chrome via Selenium 4's built-in Selenium Manager, which downloads a matching chromedriver automatically -- no separate driver install needed)

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

No `.env` file or extra config is required. `config/config.py` reads `BASE_URL`, `API_BASE_URL`, `USER_ID`, `DEFAULT_TIMEOUT`, `HEADLESS`, and `WINDOW_SIZE` from environment variables where present, falling back to defaults for this assignment (target app, `candidate-7PeYkDh0CI` user id, headless Chrome).

## Running the tests

Run everything:

```bash
pytest
```

Run only the UI suite:

```bash
pytest -m ui
```

Run only the API suite:

```bash
pytest -m api
```

Each suite runs independently -- `pytest -m ui` never touches the `requests`-based API clients beyond the shared balance-reset fixture, and `pytest -m api` never launches a browser.

To watch the browser instead of running headless, set `HEADLESS=false`:

```bash
HEADLESS=false pytest -m ui
```

## Allure reporting

Generate raw results while running tests:

```bash
pytest --alluredir=allure-results
```

Then generate and open the HTML report (requires the [Allure commandline](https://allurereport.org/docs/install/) -- e.g. `brew install allure` on macOS):

```bash
allure serve allure-results
```

or, to write a static report to disk instead of serving it:

```bash
allure generate allure-results --output allure-report --clean
allure open allure-report
```

## Project structure and architecture notes

The project follows a classic Page Object Model for the UI side (`page_objects/`, aggregated by a single `App` entity in `app/app.py` that tests interact with via one `app` fixture) and a thin client-per-resource layer for the API side (`api/`, each client subclassing a shared `BaseClient` that owns the `requests.Session`, base URL, and `x-user-id` header). `config/config.py` is a plain class rather than a fixture so both layers -- and any script -- can import it directly. Fixtures are split by scope: `tests/conftest.py` holds what UI and API share (an autouse balance reset before each test, for deterministic stakes/balances regardless of run order), while `tests/ui/conftest.py` and `tests/api/conftest.py` own their own driver/app and client fixtures respectively. Only two tests are implemented, intentionally, per the assignment's scope: one UI E2E test for the single highest-value journey (placing a bet), and one API test for a business rule (minimum stake validation) that is cheaper and more deterministic to verify below the UI. Both tests document known application defects by asserting the spec-correct expected values rather than working around them, so they fail while those defects are present.
