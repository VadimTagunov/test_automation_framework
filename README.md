# test_automation_framework

Test automation for the betting app: UI (Selenium) and API (requests) coverage for `pytest`.

## Features

- Selenium-based UI automation and `requests`-based API automation in one framework
- Built-in Allure reporting -- every meaningful action logs an Allure step, and to stdlib `logging` at the same time, so it's visible in the console even without generating a report
- `ui` / `api` pytest markers so either suite runs independently
- Page Object Model with a reusable `Element` wrapper, so pages expose intent-level methods instead of raw locators scattered across tests
- Automatic screenshot capture on UI test failure, attached straight to the Allure report
- Thread-safe `DriverManager` for the active WebDriver, so element code stays safe if tests ever run in parallel
- Central `Config` class reading from environment variables with sensible defaults, importable from anywhere in the codebase

## Prerequisites

- Python 3.9+
- Google Chrome installed locally (the UI suite drives Chrome via Selenium 4's built-in Selenium Manager, which downloads a matching chromedriver automatically -- no separate driver install needed)
- [Homebrew](https://brew.sh) and the [Allure commandline](https://allurereport.org/docs/install/) -- only needed to view the Allure HTML report, not to run the tests themselves. The Allure commandline is a Java application, so it needs a JRE; `brew install allure` pulls one in automatically (as the `openjdk` dependency) if you don't already have one:

  ```bash
  brew install allure
  ```

## Setup

```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

No `.env` file or extra config is required. `config/config.py` reads `BASE_URL`, `API_BASE_URL`, `USER_ID`, `DEFAULT_TIMEOUT`, `HEADLESS`, and `WINDOW_SIZE` from environment variables where present, falling back to defaults for this assignment (target app, `candidate-7PeYkDh0CI` user id, headless Chrome).

## Project structure

```
src/
├── api/                      # requests-based client layer, one class per resource
│   ├── base/
│   │   └── base_client.py    # requests.Session, base URL, x-user-id header, get/post/put/delete + request/response logging
│   ├── matches_client.py     # GET /api/matches
│   ├── balance_client.py     # GET /api/balance, POST /api/reset-balance
│   └── bets_client.py        # POST /api/place-bet
├── ui/
│   ├── app/
│   │   └── app.py            # App entity: aggregates all page objects for the `app` fixture
│   ├── driver/
│   │   └── manager.py        # DriverManager: thread-local registry of the active WebDriver
│   └── page_object/          # classic Page Object Model
│       ├── base/
│       │   ├── base_page.py  # shared page-object base class
│       │   └── element.py    # Element: locator + all interaction logic (click/type/get_text/wait/...)
│       ├── match_list_page.py
│       ├── bet_slip_page.py
│       └── receipt_modal.py
└── support/
    └── step.py                # step: allure.step + stdlib logging combined, usable as decorator or context manager

config/
└── config.py                  # Config: BASE_URL, USER_ID, timeouts, etc. (env vars with fallback defaults)

tests/
├── conftest.py                # shared fixtures -- autouse balance reset before every test
├── ui/
│   ├── conftest.py            # driver/app fixtures; attaches a screenshot to Allure on failure
│   └── test_place_bet.py      # UI E2E: successful single bet placement
└── api/
    ├── conftest.py            # API client fixtures
    └── test_place_bet_api.py  # API: stake below minimum -> 422 invalid_stake_min

pytest.ini                     # markers, --alluredir default, live log config
requirements.txt
```

Only two tests are implemented, intentionally, per the assignment's scope: the single highest-value UI journey (placing a bet) and one API-level business rule (minimum stake validation) that's cheaper and more deterministic to verify below the UI. Both assert the spec-correct expected values even where known application defects would make that assertion fail, so they document real product behavior rather than working around it. `test-plan.md`, `execution-results.md`, `strategy-and-recommendations.md`, and `bugs_screenshots/` at the repo root cover the manual QA work and the reasoning behind those two automation choices.

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

Generate the HTML report from those results:

```bash
allure generate allure-results --output allure-report --clean
```

Then open it:

```bash
allure open allure-report
```

Or skip the generate/open split and serve it directly in one step:

```bash
allure serve allure-results
```
