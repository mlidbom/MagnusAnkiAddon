from __future__ import annotations
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any, Optional
import logging
import os
from aqt import mw
from anki.hooks import wrap
from aqt.addons import AddonManager

def is_testing() -> bool: return "pytest" in sys.modules

def log_file_path(addon: str) -> Path:
    logs_dir = Path(mw.addonManager.addonsFolder(addon)) / "user_files" / "logs"
    logs_dir.mkdir(parents=True, exist_ok=True)
    return logs_dir / f"{addon}.log"

def get_logger(module: str) -> logging.Logger:
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

    file_handler: Optional[RotatingFileHandler] = None

    # Prevent errors when deleting/updating the add-on on Windows
    # noinspection PyUnusedLocal
    def close_log_file(manager: AddonManager, m: str, *args: Any, **kwargs: Any) -> None:
        if m == addon and file_handler:
            file_handler.close()

    if not is_testing():
        log_path = log_file_path(addon)
        # noinspection PyArgumentEqualDefault
        file_handler = RotatingFileHandler(str(log_path), "a", encoding="utf-8", maxBytes=3 * 1024 * 1024, backupCount=5, )
        file_formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        file_handler.setFormatter(file_formatter)
        logger.addHandler(file_handler)

        AddonManager.deleteAddon = wrap(  # type: ignore[method-assign]
            AddonManager.deleteAddon, close_log_file, "before"
        )
        AddonManager.backupUserFiles = wrap(  # type: ignore[method-assign]
            AddonManager.backupUserFiles, close_log_file, "before"
        )

    return logger


_addon_name = os.path.basename(os.path.dirname(__file__))
log = get_logger(_addon_name)
