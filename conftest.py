# content of conftest.py

from multiprocessing import RLock

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--slow", action="store_true", default=False, help="run slow tests"
    )


def pytest_collection_modifyitems(config, items):
    if config.getoption("--slow"):
        # --slow given in cli: do not skip slow tests
        return
    lock = RLock()
    with lock:
        for item in items:
            if "slow" in item.keywords:
                item.add_marker(pytest.mark.skip(reason="need --slow option to run"))
