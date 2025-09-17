from __future__ import annotations

from typing import TYPE_CHECKING

from ex_autoslot import ProfilableAutoSlots

if TYPE_CHECKING:
    from anki.config import ConfigManager


class ConfigManagerEx(ProfilableAutoSlots):
    def __init__(self, config:ConfigManager) -> None:
        self.config: ConfigManager = config

    def set_timebox_seconds(self, seconds:int) -> None:
        self.config.set("timeLim", seconds)