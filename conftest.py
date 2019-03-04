# content of conftest.py

from multiprocessing import RLock

import pytest


def pytest_addoption(parser):
    parser.addoption(
        "--slow",
        action="store_true",
        default=False,
        help="only slow tests (only non-slow by default)",
    )


def pytest_collection_modifyitems(config, items):
    slow_toggle = bool(config.getoption("--slow"))
    lock = RLock()
    with lock:
        for item in items:
            slow_present = "slow" in item.keywords
            if slow_toggle != slow_present:
                item.add_marker(
                    pytest.mark.skip(reason=f"[--slow {slow_toggle}, {slow_present}]")
                )
    return
