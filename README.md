# test_automation_framework

Test automation for the betting app: UI (Selenium) and API (requests) coverage for `pytest`.

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

## Project structure and architecture notes

Source code lives under `src/`, split into `src/api/` and `src/ui/`. The UI side follows a classic Page Object Model: `src/ui/page_object/` holds the pages, aggregated by a single `App` entity in `src/ui/app/app.py` that tests interact with via one `app` fixture, and `src/ui/driver/manager.py` holds `DriverManager`, the thread-local registry of the active Selenium driver. The API side is a thin client-per-resource layer (`src/api/`), each client subclassing a shared `BaseClient` that owns the `requests.Session`, base URL, and `x-user-id` header. Both sides keep their shared base class in its own `base/` subpackage (`src/api/base/base_client.py`, `src/ui/page_object/base/base_page.py`), separate from the concrete clients/pages that build on it. Each page object initializes its elements as plain instance attributes in its constructor, wrapping each locator in a small `Element` (`src/ui/page_object/base/element.py`) that owns all interaction logic (click, type, get text/attribute, wait for visibility) and re-locates on every call rather than caching a stale reference. `Element` does not take a driver in its constructor -- it fetches the active one from `DriverManager`, which the UI `driver` fixture populates, so element code stays driver-agnostic and safe if tests ever run across multiple threads in parallel. `config/config.py` is a plain class rather than a fixture so both layers -- and any script -- can import it directly. Fixtures are split by scope: `tests/conftest.py` holds what UI and API share (an autouse balance reset before each test, for deterministic stakes/balances regardless of run order), while `tests/ui/conftest.py` and `tests/api/conftest.py` own their own driver/app and client fixtures respectively. Only two tests are implemented, intentionally, per the assignment's scope: one UI E2E test for the single highest-value journey (placing a bet), and one API test for a business rule (minimum stake validation) that is cheaper and more deterministic to verify below the UI. Both tests document known application defects by asserting the spec-correct expected values rather than working around them, so they fail while those defects are present.
