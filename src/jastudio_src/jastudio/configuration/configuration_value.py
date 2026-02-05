from __future__ import annotations

from typing import TYPE_CHECKING

from aqt import mw
from JAStudio.Core import Configuration

from jastudio.ankiutils import app

if TYPE_CHECKING:
    from JAStudio.Core.Configuration import JapaneseConfig
    from jaspythonutils.sysutils.lazy import Lazy

def _get_config_dict() -> dict[str, object]:
    return mw.addonManager.getConfig(app.addon_name) or {} if not app.is_testing else {}

def _write_config_dict(config_dict: dict[str, object]) -> None:
    if not app.is_testing:
        mw.addonManager.writeConfig(app.addon_name, config_dict)  # pyright: ignore[reportUnknownMemberType]

Configuration.Init(_get_config_dict, _write_config_dict)

config: Lazy[JapaneseConfig] = Configuration.Config
