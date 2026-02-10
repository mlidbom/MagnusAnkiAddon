from __future__ import annotations

import json

from aqt import mw

from jastudio.ankiutils import app


def _get_config_dict() -> dict[str, object]:
    return mw.addonManager.getConfig(app.addon_name) or {} if not app.is_testing else {}

def _write_config_dict(config_dict: dict[str, object]) -> None:
    if not app.is_testing:
        mw.addonManager.writeConfig(app.addon_name, config_dict)  # pyright: ignore[reportUnknownMemberType]

def write_config_dict_json(config_dict_json: str) -> None:
    _write_config_dict(json.loads(config_dict_json))  # pyright: ignore[reportAny]

def get_config_json() -> str:
    """Return the Anki addon config as a JSON string (for passing to C#)."""
    return json.dumps(_get_config_dict(), indent=3, ensure_ascii=False)
