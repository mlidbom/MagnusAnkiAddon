from __future__ import annotations

from ankiutils import app


class ConfigurationCache:
    _instance: ConfigurationCache | None = None
    _initialized: bool = False
    def __init__(self) -> None:
        self._hide_transparent_compounds: bool = app.config().hide_compositionally_transparent_compounds.get_value()
        self._hide_all_compounds: bool = app.config().hide_all_compounds.get_value()

        if not ConfigurationCache._initialized:
            app.config().hide_compositionally_transparent_compounds.on_change(self._replace_instance)
            app.config().hide_all_compounds.on_change(self._replace_instance)
            ConfigurationCache._initialized = True

    @staticmethod
    def hide_transparent_compounds() -> bool: return ConfigurationCache._get_instance()._hide_transparent_compounds
    @staticmethod
    def hide_all_compounds() -> bool: return ConfigurationCache._get_instance()._hide_all_compounds

    @staticmethod
    def _get_instance() -> ConfigurationCache:
        if ConfigurationCache._instance is None:
            ConfigurationCache._instance = ConfigurationCache()
        return ConfigurationCache._instance

    @staticmethod
    def _replace_instance(_: object) -> None:
        ConfigurationCache._instance = ConfigurationCache()
