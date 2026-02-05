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

# Initialize C# configuration system using PythonInterop shim
from jaslib import mylog
from JAStudio.Core.Configuration import ConfigurationValue  # pyright: ignore[reportMissingImports]
from JAStudio.PythonInterop import PythonDotNetShim  # pyright: ignore[reportMissingImports]

# Convert Python dict and callable to .NET types using shim
cs_config_dict = PythonDotNetShim.ToDotNetDict(_get_config_dict())  # pyright: ignore[reportUnknownMemberType]
cs_update_callback = PythonDotNetShim.ToDotNetDictAction(_write_config_dict)  # pyright: ignore[reportUnknownMemberType]

ConfigurationValue.Init(cs_config_dict, cs_update_callback)  # pyright: ignore[reportUnknownMemberType]
mylog.info("C# ConfigurationValue initialized successfully")

config: Lazy[JapaneseConfig] = configuration_value.config
