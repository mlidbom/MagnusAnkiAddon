from __future__ import annotations

import os
from typing import TYPE_CHECKING

from jaslib.testutils import ex_pytest
from jaspythonutils.sysutils.lazy import Lazy

if TYPE_CHECKING:
    import logging

def is_testing() -> bool:
    import sys
    return "pytest" in sys.modules

# noinspection DuplicatedCode
def get_logger() -> logging.Logger:
    import logging
    import sys


    logger = logging.getLogger("addon")

    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setLevel(logging.DEBUG if "ANKIDEV" in os.environ else logging.INFO)
    stdout_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stdout_handler.setFormatter(stdout_formatter)
    logger.addHandler(stdout_handler)

    return logger

_logger: Lazy[logging.Logger] = Lazy(lambda: get_logger())

def debug(msg: str) -> None:
    if not ex_pytest.is_testing: _logger().debug(msg)
def info(msg: str) -> None:
    if not ex_pytest.is_testing: _logger().info(msg)
def warning(msg: str) -> None: _logger().warning(msg)
def error(msg: str) -> None: _logger().error(msg)

def set_logger_factory(logger: Lazy[logging.Logger]) -> None:
    global _logger
    _logger = logger
