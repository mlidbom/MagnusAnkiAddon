from __future__ import annotations

import json
from typing import TYPE_CHECKING

from aqt import mw
from jaslib import mylog
from jaslib.configuration import configuration_value
from JAStudio.Core import App
from System import Action

from jastudio.ankiutils import app

if TYPE_CHECKING:
    from jaslib.configuration.configuration_value import JapaneseConfig
    from jaspythonutils.sysutils.lazy import Lazy

def _get_config_dict() -> dict[str, object]:
    return mw.addonManager.getConfig(app.addon_name) or {} if not app.is_testing else {}

def _write_config_dict(config_dict: dict[str, object]) -> None:
    if not app.is_testing:
        mw.addonManager.writeConfig(app.addon_name, config_dict)  # pyright: ignore[reportUnknownMemberType]

def _write_config_dict_json(config_dict_json: str) -> None:
    _write_config_dict(json.loads(config_dict_json))  # pyright: ignore[reportAny]

# Initialize Python configuration system
configuration_value.init(_get_config_dict(), _write_config_dict)

# Initialize C# configuration system
_callback = Action[str](_write_config_dict_json)  # pyright: ignore [reportCallIssue]
_json_dict = json.dumps(_get_config_dict(), indent=3, ensure_ascii=False)
App.InitConfigJson(_json_dict, _callback)
mylog.info("C# ConfigurationValue initialized successfully")

config: Lazy[JapaneseConfig] = configuration_value.config
