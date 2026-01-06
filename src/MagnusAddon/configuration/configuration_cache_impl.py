from __future__ import annotations

from ankiutils import app


class ConfigurationCache:
    _instance: ConfigurationCache | None = None
    _initialized: bool = False
    def __init__(self) -> None:
        self._hide_transparent_compounds: bool = app.config().hide_compositionally_transparent_compounds.get_value()
        self._hide_all_compounds: bool = app.config().hide_all_compounds.get_value()
        self._show_breakdown_in_edit_mode: bool = app.config().show_sentence_breakdown_in_edit_mode.get_value()

        if not ConfigurationCache._initialized:
            app.config().on_change(self._replace_instance)
            ConfigurationCache._initialized = True

    @classmethod
    def hide_transparent_compounds(cls) -> bool: return ConfigurationCache._get_instance()._hide_transparent_compounds
    @classmethod
    def hide_all_compounds(cls) -> bool: return ConfigurationCache._get_instance()._hide_all_compounds
    @classmethod
    def show_breakdown_in_edit_mode(cls) -> bool: return ConfigurationCache._get_instance()._show_breakdown_in_edit_mode

    @classmethod
    def _get_instance(cls) -> ConfigurationCache:
        if ConfigurationCache._instance is None:
            ConfigurationCache._instance = ConfigurationCache()
        return ConfigurationCache._instance

    @classmethod
    def _replace_instance(cls) -> None:
        ConfigurationCache._instance = ConfigurationCache()
