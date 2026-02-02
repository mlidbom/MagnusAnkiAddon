from __future__ import annotations

import os
from typing import TYPE_CHECKING

from aqt import mw
from jaslib.configuration import configuration_value
from jastudio.ankiutils import app

if TYPE_CHECKING:
    from jaslib.configuration.configuration_value import JapaneseConfig
    from jaslib.sysutils.lazy import Lazy

_addon_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
_addon_name = os.path.basename(_addon_dir)

def _get_config_dict() -> dict[str, object]:
    return mw.addonManager.getConfig(_addon_name) or {} if not app.is_testing else {}


def _write_config_dict(config_dict: dict[str, object]) -> None:
    if not app.is_testing:
        mw.addonManager.writeConfig(_addon_name, config_dict)  # pyright: ignore[reportUnknownMemberType]


configuration_value.init(_get_config_dict(), _write_config_dict)


config: Lazy[JapaneseConfig] = configuration_value.config
