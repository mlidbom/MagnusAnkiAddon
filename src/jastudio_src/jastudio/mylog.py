from __future__ import annotations

import os
from typing import TYPE_CHECKING

from jastudio.sysutils.lazy import Lazy
from jastudio.testutils import ex_pytest

if TYPE_CHECKING:
    import logging
    from logging.handlers import RotatingFileHandler
    from pathlib import Path

def is_testing() -> bool:
    import sys
    return "pytest" in sys.modules

def log_file_path(addon: str) -> Path:
    from pathlib import Path

    from aqt import mw
    logs_dir = Path(mw.addonManager.addonsFolder(addon)) / "user_files" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir / f"{addon}.log"

def get_logger(module: str) -> logging.Logger:
    import logging
    import sys
    from logging.handlers import RotatingFileHandler

    from anki.hooks import wrap  # pyright: ignore[reportUnknownVariableType]
    from aqt import mw
    from aqt.addons import AddonManager
    addon = ""
    if is_testing():
        logger = logging.getLogger("addon")
    else:
        addon = mw.addonManager.addonFromModule(module)
        logger = logging.getLogger(addon)
    logger.setLevel(logging.DEBUG)
    logger.propagate = False

    stdout_handler = logging.StreamHandler(stream=sys.stdout)
    stdout_handler.setLevel(logging.DEBUG if "ANKIDEV" in os.environ else logging.INFO)
    stdout_formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
    stdout_handler.setFormatter(stdout_formatter)
    logger.addHandler(stdout_handler)

    file_handler: RotatingFileHandler | None = None

    # Prevent errors when deleting/updating the add-on on Windows
    # noinspection PyUnusedLocal
    def close_log_file(manager: AddonManager, m: str, *args: object, **kwargs: object) -> None:  # pyright: ignore[reportUnusedParameter]
        if m == addon and file_handler:
            file_handler.close()

    if not is_testing():
        log_path = log_file_path(addon)
        # noinspection PyArgumentEqualDefault
        file_handler = RotatingFileHandler(str(log_path), "a", encoding="utf-8", maxBytes=3 * 1024 * 1024, backupCount=5, )
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        AddonManager.deleteAddon = wrap(  # type: ignore
            AddonManager.deleteAddon, close_log_file, "before"
        )
        AddonManager.backupUserFiles = wrap( # type: ignore
            AddonManager.backupUserFiles, close_log_file, "before"
        )

    return logger

_addon_folder_name = os.path.basename(os.path.dirname(__file__))
_logger: Lazy[logging.Logger] = Lazy(lambda: get_logger(_addon_folder_name))

def debug(msg: str) -> None:
    if not ex_pytest.is_testing: _logger().debug(msg)
def info(msg: str) -> None:
    if not ex_pytest.is_testing: _logger().info(msg)
def warning(msg: str) -> None: _logger().warning(msg)
def error(msg: str) -> None: _logger().error(msg)
