from __future__ import annotations

from typing import TYPE_CHECKING

from aqt import mw
from jaslib.configuration import configuration_value

from jastudio.ankiutils import app

if TYPE_CHECKING:
    from jaslib.configuration.configuration_value import JapaneseConfig
    from jaspythonutils.sysutils.lazy import Lazy

def _get_config_dict() -> dict[str, object]:
    return mw.addonManager.getConfig(app.addon_name) or {} if not app.is_testing else {}

def _write_config_dict(config_dict: dict[str, object]) -> None:
    if not app.is_testing:
        mw.addonManager.writeConfig(app.addon_name, config_dict)  # pyright: ignore[reportUnknownMemberType]

# Initialize Python configuration system
configuration_value.init(_get_config_dict(), _write_config_dict)

# Initialize C# configuration system
from JAStudio.Core.Configuration import ConfigurationValue  # pyright: ignore[reportMissingImports]
from System import Action  # pyright: ignore[reportMissingImports]
from System.Collections.Generic import Dictionary  # pyright: ignore[reportMissingImports]
from jaslib import mylog

# Convert Python dict to C# Dictionary
DictType = Dictionary[str, object]  # Get the instantiated generic type
cs_config_dict = DictType()  # Create instance
for key, value in _get_config_dict().items():
    cs_config_dict[key] = value  # pyright: ignore[reportIndexIssue]

# Create C# callback for config updates
def cs_write_callback(cs_dict: object) -> None:
    # Convert C# dict back to Python dict and write
    python_dict = {k: cs_dict[k] for k in cs_dict.Keys}  # pyright: ignore[reportUnknownMemberType, reportUnknownArgumentType]
    _write_config_dict(python_dict)

ActionType = Action[DictType]  # Get the instantiated Action type
cs_update_action = ActionType(cs_write_callback)

ConfigurationValue.Init(cs_config_dict, cs_update_action)  # pyright: ignore[reportUnknownMemberType]
mylog.info("C# ConfigurationValue initialized successfully")

config: Lazy[JapaneseConfig] = configuration_value.config
