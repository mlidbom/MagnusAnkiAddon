from __future__ import annotations


class Settings:
    _instance: Settings | None = None
    _initialized: bool = False
    def __init__(self) -> None:
        from ankiutils import app
        self._hide_transparent_compounds: bool = app.config().hide_compositionally_transparent_compounds.get_value()
        self._show_breakdown_in_edit_mode: bool = app.config().show_sentence_breakdown_in_edit_mode.get_value()
        self._hide_all_compounds: bool = app.config().hide_all_compounds.get_value()
        self._log_when_flushing_notes: bool = app.config().log_when_flushing_notes.get_value()

        if not Settings._initialized:
            app.config().on_change(self._replace_instance)
            Settings._initialized = True

    @classmethod
    def hide_transparent_compounds(cls) -> bool: return Settings._get_instance()._hide_transparent_compounds
    @classmethod
    def hide_all_compounds(cls) -> bool: return Settings._get_instance()._hide_all_compounds
    @classmethod
    def show_breakdown_in_edit_mode(cls) -> bool: return Settings._get_instance()._show_breakdown_in_edit_mode
    @classmethod
    def log_when_flushing_notes(cls) -> bool: return Settings._get_instance()._log_when_flushing_notes

    @classmethod
    def _get_instance(cls) -> Settings:
        if Settings._instance is None:
            Settings._instance = Settings()
        return Settings._instance

    @classmethod
    def _replace_instance(cls) -> None:
        Settings._instance = Settings()
