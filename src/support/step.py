"""Combined Allure step + stdlib logging helper.

allure.step() only ever writes structured JSON into the Allure results
directory (created by `pytest --alluredir=...`) -- it never prints
anything to the console or to Python's logging output. `step` is a
drop-in replacement, usable both as a decorator and as a context
manager exactly like allure.step, that additionally emits an INFO log
record for every step through the standard `logging` module. With
pytest's log capturing enabled (see pytest.ini), that record shows up
in the terminal / test runner output even when no Allure report is ever
generated.
"""
from __future__ import annotations

import functools
import inspect
import logging
from typing import Any, Callable

import allure

logger = logging.getLogger("test_automation_framework")


class step:
    def __init__(self, title: str) -> None:
        self.title = title
        self._allure_step: allure.step | None = None

    def __call__(self, func: Callable) -> Callable:
        signature = inspect.signature(func)

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            bound = signature.bind(*args, **kwargs)
            bound.apply_defaults()
            message = self.title.format(**bound.arguments)
            with step(message):
                return func(*args, **kwargs)

        return wrapper

    def __enter__(self) -> "step":
        logger.info(self.title)
        self._allure_step = allure.step(self.title)
        self._allure_step.__enter__()
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._allure_step.__exit__(exc_type, exc_val, exc_tb)
