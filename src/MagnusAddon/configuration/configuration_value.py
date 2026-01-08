from __future__ import annotations

import os
from typing import TYPE_CHECKING, cast

from ankiutils import app
from aqt import mw
from autoslot import Slots  # pyright: ignore[reportMissingTypeStubs]
from sysutils.lazy import Lazy
from sysutils.typed import non_optional
from sysutils.weak_ref import WeakRefable

if TYPE_CHECKING:
    from collections.abc import Callable

_addon_dir = os.path.dirname(os.path.dirname(__file__))
_addon_name = os.path.basename(_addon_dir)

def _get_config_dict() -> dict[str, object]:
    return mw.addonManager.getConfig(_addon_name) or {} if not app.is_testing else {}

_config_dict: Lazy[dict[str, object]] = Lazy(_get_config_dict)

def _write_config_dict() -> None:
    if not app.is_testing:
        mw.addonManager.writeConfig(_addon_name, _config_dict())  # pyright: ignore[reportUnknownMemberType]

class ConfigurationValue[T](WeakRefable, Slots):
    def __init__(self, name: str, title: str, default: T, feature_toggler: Callable[[T], None] | None = None) -> None:
        self.title: str = title
        self.feature_toggler: Callable[[T], None] | None = feature_toggler
        self.name: str = name
        self._value: T = cast(T, _config_dict().get(name, default))

        if self.feature_toggler:
            app.add_init_hook(self.toggle_feature)

        self._change_callbacks: list[Callable[[T], None]] = []

    def get_value(self) -> T:
        return self._value

    def set_value(self, value: T) -> None:
        self._value = value
        _config_dict()[self.name] = value
        self.toggle_feature()
        _write_config_dict()
        for callback in self._change_callbacks:
            callback(self.get_value())

    def on_change(self, callback: Callable[[T], None]) -> None:
        self._change_callbacks.append(callback)

    def toggle_feature(self) -> None:
        if self.feature_toggler is not None:
            self.feature_toggler(self._value)

ConfigurationValueInt = ConfigurationValue[int]
ConfigurationValueFloat = ConfigurationValue[float]
ConfigurationValueBool = ConfigurationValue[bool]

class JapaneseConfig(Slots):
    def __init__(self) -> None:
        self._change_callbacks: list[Callable[[], None]] = []

        def add_float(value: ConfigurationValueFloat) -> ConfigurationValueFloat:
            value.on_change(lambda _: self._publish_change())
            return value

        def add_int(value: ConfigurationValueInt) -> ConfigurationValueInt:
            value.on_change(lambda _: self._publish_change())
            return value

        def add_bool(value: ConfigurationValueBool) -> ConfigurationValueBool:
            value.on_change(lambda _: self._publish_change())
            return value

        self.boost_failed_card_allowed_time_by_factor: ConfigurationValueFloat = add_float(ConfigurationValueFloat("boost_failed_card_allowed_time_by_factor", "Boost Failed Card Allowed Time Factor", 1.5))
        self.boost_failed_card_allowed_time: ConfigurationValueBool = ConfigurationValueBool("boost_failed_card_allowed_time", "Boost failed card allowed time", True)

        def set_enable_fsrs_short_term_with_steps(toggle: bool) -> None:
            # noinspection PyProtectedMember, PyArgumentList
            non_optional(mw.col)._set_enable_fsrs_short_term_with_steps(toggle)  # pyright: ignore[reportPrivateUsage]

        self.autoadvance_vocab_starting_seconds: ConfigurationValueFloat = add_float(ConfigurationValueFloat("autoadvance_vocab_starting_seconds", "Starting Seconds", 3.0))
        self.autoadvance_vocab_hiragana_seconds: ConfigurationValueFloat = add_float(ConfigurationValueFloat("autoadvance_vocab_hiragana_seconds", "Hiragana Seconds", 0.7))
        self.autoadvance_vocab_katakana_seconds: ConfigurationValueFloat = add_float(ConfigurationValueFloat("autoadvance_vocab_katakana_seconds", "Katakana Seconds", 0.7))
        self.autoadvance_vocab_kanji_seconds: ConfigurationValueFloat = add_float(ConfigurationValueFloat("autoadvance_vocab_kanji_seconds", "Kanji Seconds", 1.5))

        self.autoadvance_sentence_starting_seconds: ConfigurationValueFloat = add_float(ConfigurationValueFloat("autoadvance_sentence_starting_seconds", "Starting Seconds", 3.0))
        self.autoadvance_sentence_hiragana_seconds: ConfigurationValueFloat = add_float(ConfigurationValueFloat("autoadvance_sentence_hiragana_seconds", "Hiragana Seconds", 0.7))
        self.autoadvance_sentence_katakana_seconds: ConfigurationValueFloat = add_float(ConfigurationValueFloat("autoadvance_sentence_katakana_seconds", "Katakana Seconds", 0.7))
        self.autoadvance_sentence_kanji_seconds: ConfigurationValueFloat = add_float(ConfigurationValueFloat("autoadvance_sentence_kanji_seconds", "Kanji Seconds", 1.5))

        self.timebox_vocab_read: ConfigurationValueInt = add_int(ConfigurationValueInt("time_box_length_vocab_read", "Vocab Read", 15))
        self.timebox_vocab_listen: ConfigurationValueInt = add_int(ConfigurationValueInt("time_box_length_vocab_listen", "Vocab Listen", 15))
        self.timebox_sentence_read: ConfigurationValueInt = add_int(ConfigurationValueInt("time_box_length_sentence_read", "Sentence Read", 15))
        self.timebox_sentence_listen: ConfigurationValueInt = add_int(ConfigurationValueInt("time_box_length_sentence_listen", "Sentence Listen", 15))
        self.timebox_kanji_read: ConfigurationValueInt = add_int(ConfigurationValueInt("time_box_length_kanji", "Kanji", 15))
        self.yomitan_integration_copy_answer_to_clipboard: ConfigurationValueBool = add_bool(ConfigurationValueBool("yomitan_integration_copy_answer_to_clipboard", "Yomitan integration: Copy reviewer answer to clipboard", False))

        self.anki_internal_fsrs_set_enable_fsrs_short_term_with_steps: ConfigurationValueBool = ConfigurationValueBool("fsrs_set_enable_fsrs_short_term_with_steps",
                                                                                                                       "FSRS: Enable short term scheduler with steps",
                                                                                                                       default=False,
                                                                                                                       feature_toggler=set_enable_fsrs_short_term_with_steps)

        self.decrease_failed_card_intervals: ConfigurationValueBool = add_bool(ConfigurationValueBool("decrease_failed_card_intervals", "Decrease failed card intervals", False))

        self.prevent_double_clicks: ConfigurationValueBool = add_bool(ConfigurationValueBool("prevent_double_clicks", "Prevent double clicks", True))
        self.prefer_default_mnemonics_to_source_mnemonics: ConfigurationValueBool = add_bool(ConfigurationValueBool("prefer_default_mnemocs_to_source_mnemonics", "Prefer default mnemonics to source mnemonics", False))

        self.show_compound_parts_in_sentence_breakdown: ConfigurationValueBool = add_bool(ConfigurationValueBool("show_compound_parts_in_sentence_breakdown", "Show compound parts in sentence breakdown", True))
        self.show_kanji_in_sentence_breakdown: ConfigurationValueBool = add_bool(ConfigurationValueBool("show_kanji_in_sentence_breakdown", "Show kanji in sentence breakdown", True))
        self.show_sentence_breakdown_in_edit_mode: ConfigurationValueBool = add_bool(ConfigurationValueBool("show_sentence_breakdown_in_edit_mode", "Show sentence breakdown in edit mode", False))
        self.automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound: ConfigurationValueBool = add_bool(ConfigurationValueBool("automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound",
                                                                                                                                                     "Automatically yield last token in suru verb compounds to overlapping compounds (Ctrl+Shift+Alt+s)", True))
        self.automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound: ConfigurationValueBool = add_bool(ConfigurationValueBool("automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound",
                                                                                                                                                        "Automatically yield last token in passive verb compounds to overlapping compounds (Ctrl+Shift+Alt+h)", True))
        self.automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound: ConfigurationValueBool = add_bool(ConfigurationValueBool("automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound",
                                                                                                                                                          "Automatically yield last token in causative verb compounds to overlapping compounds (Ctrl+Shift+Alt+t)", True))

        self.decrease_failed_card_intervals_interval: ConfigurationValueInt = add_int(ConfigurationValueInt("decrease_failed_card_intervals_interval", "Failed card again seconds for next again", 60))

        self.minimum_time_viewing_question: ConfigurationValueFloat = add_float(ConfigurationValueFloat("minimum_time_viewing_question", "Minimum time viewing question", 0.5))
        self.minimum_time_viewing_answer: ConfigurationValueFloat = add_float(ConfigurationValueFloat("minimum_time_viewing_answer", "Minimum time viewing answer", 0.5))
        self.hide_compositionally_transparent_compounds: ConfigurationValueBool = add_bool(ConfigurationValueBool("hide_compositionally_transparent_compounds", "Hide compositionally transparent compounds", True))
        self.hide_all_compounds: ConfigurationValueBool = add_bool(ConfigurationValueBool("hide_all_compounds", "Hide all compounds", False))

        self.sentence_view_toggles: list[ConfigurationValueBool] = [self.automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound,
                                                                    self.automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound,
                                                                    self.automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound,
                                                                    self.hide_compositionally_transparent_compounds,
                                                                    self.hide_all_compounds,
                                                                    self.show_compound_parts_in_sentence_breakdown,
                                                                    self.show_sentence_breakdown_in_edit_mode,
                                                                    self.show_kanji_in_sentence_breakdown]

        # performance
        self.load_jamdict_db_into_memory: ConfigurationValueBool = add_bool(ConfigurationValueBool("load_jamdict_db_into_memory", "Load Jamdict DB into memory [Requires restart]", False))
        self.pre_cache_card_studying_status: ConfigurationValueBool = add_bool(ConfigurationValueBool("pre_cache_card_studying_status", "Cache card studying status on startup. Only disable for dev/testing purposes. [Requires restart]", False))
        self.prevent_anki_from_garbage_collecting_every_time_a_window_closes: ConfigurationValueBool = add_bool(ConfigurationValueBool("prevent_anki_from_garbage_collecting_every_time_a_window_closes", "Prevent Anki from garbage collecting every time a window closes, causing a short hang every time. [Requires restart]", True))
        self.disable_all_automatic_garbage_collection: ConfigurationValueBool = add_bool(ConfigurationValueBool("disable_periodic_garbage_collection", "Prevent all automatic garbage collection. Will stop the mini-hangs but memory usage will grow gradually. [Requires restart]", False))
        self.load_studio_in_foreground: ConfigurationValueBool = add_bool(ConfigurationValueBool("load_studio_in_foreground", "Load Studio in foreground. Makes it clear when done. Anki will be responsive when done. But you can't use anki while loading.", True))

        # memory
        self.enable_garbage_collection_during_batches: ConfigurationValueBool = add_bool(ConfigurationValueBool("enable_garbage_collection_during_batches", "Enable Batch GC. [Requires restart]", True))
        self.enable_automatic_garbage_collection: ConfigurationValueBool = add_bool(ConfigurationValueBool("enable_automatic_garbage_collection", "Enable automatic GC. [Requires restart. Reduces memory usage the most but slows Anki down and may cause crashes due to Qt incompatibility.]", False))
        self.track_instances_in_memory: ConfigurationValueBool = add_bool(ConfigurationValueBool("track_instances_in_memory", "Track instances in memory. [Requires restart.. Only useful to developers and will use extra memory.]", False))
        self.enable_auto_string_interning: ConfigurationValueBool = add_bool(ConfigurationValueBool("enable_auto_string_interning", "Enable automatic string interning. Reduces memory usage at the cost of some CPU overhead and slowdown. [Requires restart]", False))

        self.enable_trace_malloc: ConfigurationValueBool = add_bool(ConfigurationValueBool("enable_trace_malloc", "Enable tracemalloc. Will show memory usage in logs and increase memory usage A LOT. [Requires restart]", False))
        self.log_when_flushing_notes: ConfigurationValueBool = add_bool(ConfigurationValueBool("log_when_flushing_notes", "Log when flushing notes to backend.", False))

        self.feature_toggles: list[tuple[str, list[ConfigurationValueBool]]] = \
            [("Sentence Display", self.sentence_view_toggles),
             ("Misc", [self.yomitan_integration_copy_answer_to_clipboard,
                       self.anki_internal_fsrs_set_enable_fsrs_short_term_with_steps,
                       self.decrease_failed_card_intervals,
                       self.prevent_double_clicks,
                       self.boost_failed_card_allowed_time,
                       self.prefer_default_mnemonics_to_source_mnemonics]),
             ("Performance and memory usage", [self.load_studio_in_foreground,
                                               self.load_jamdict_db_into_memory,
                                               self.pre_cache_card_studying_status,
                                               self.prevent_anki_from_garbage_collecting_every_time_a_window_closes,
                                               self.disable_all_automatic_garbage_collection,
                                               self.enable_garbage_collection_during_batches,
                                               self.enable_automatic_garbage_collection,
                                               self.enable_auto_string_interning]),
             ("Devolpers only", [self.enable_trace_malloc,
                                 self.track_instances_in_memory,
                                 self.log_when_flushing_notes])
             ]

        self.readings_mappings_dict: dict[str, str] = self._read_reading_mappings_from_file()

    def toggle_all_sentence_display_auto_yield_flags(self, value: bool | None = None) -> None:
        value = value if value is not None else not self.automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound.get_value()
        self.automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound.set_value(value)
        self.automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound.set_value(value)
        self.automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound.set_value(value)

    def save_mappings(self, mappings: str) -> None:
        mappings_file_path = self._mappings_file_path()
        with open(mappings_file_path, "w", encoding="utf-8") as f:
            f.write(mappings)

        self.readings_mappings_dict = self._read_reading_mappings_from_file()

    def set_readings_mappings_for_testing(self, mappings: str) -> None:
        self.readings_mappings_dict = self._parse_mappings_from_string(mappings)

    @classmethod
    def read_readings_mappings_file(cls) -> str:
        with open(cls._mappings_file_path(), encoding="utf-8") as f:
            return f.read()

    def _publish_change(self) -> None:
        for callback in self._change_callbacks:
            callback()

    def on_change(self, callback: Callable[[], None]) -> None:
        self._change_callbacks.append(callback)

    @classmethod
    def _read_reading_mappings_from_file(cls) -> dict[str, str]:
        return cls._parse_mappings_from_string(cls.read_readings_mappings_file())

    @classmethod
    def _parse_mappings_from_string(cls, mappings_string: str) -> dict[str, str]:
        def parse_value_part(value_part: str) -> str:
            if "<read>" in value_part:
                return value_part
            if ":" in value_part:
                parts = value_part.split(":", 1)
                return f"""<read>{parts[0].strip()}</read>{parts[1]}"""
            return f"<read>{value_part}</read>"

        return {
                line.split(":", 1)[0].strip(): parse_value_part(line.split(":", 1)[1].strip())
                for line in mappings_string.strip().splitlines()
                if ":" in line
        }

    @classmethod
    def _mappings_file_path(cls) -> str:
        return os.path.join(app.user_files_dir, "readings_mappings.txt")

config: Lazy[JapaneseConfig] = Lazy(lambda: JapaneseConfig())
