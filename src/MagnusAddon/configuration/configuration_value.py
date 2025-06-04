from __future__ import annotations

import os
from typing import Callable, Generic, Optional, TypeVar

from ankiutils import app
from aqt import mw
from autoslot import Slots
from sysutils.lazy import Lazy

T = TypeVar("T")

_addon_dir = os.path.dirname(os.path.dirname(__file__))
_addon_name = os.path.basename(_addon_dir)

_config_dict = Lazy(lambda: mw.addonManager.getConfig(_addon_name) or {})

def _write_config_dict() -> None:
    mw.addonManager.writeConfig(_addon_name, _config_dict.instance())

class ConfigurationValue(Generic[T]):
    def __init__(self, name: str, title: str, default: T, feature_toggler: Optional[Callable[[T], None]] = None) -> None:
        self.title = title
        self.feature_toggler: Optional[Callable[[T], None]] = feature_toggler
        self.name = name
        self._value: T = _config_dict.instance().get(name, default)

        if self.feature_toggler:
            app.add_init_hook(self.toggle_feature)

        self._change_callbacks: list[Callable[[T], None]] = []

    def get_value(self) -> T:
        return self._value

    def set_value(self, value: T) -> None:
        self._value = value
        _config_dict.instance()[self.name] = value
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
        self.boost_failed_card_allowed_time_by_factor = ConfigurationValueFloat("boost_failed_card_allowed_time_by_factor", "Boost Failed Card Allowed Time Factor", 1.5)
        self.boost_failed_card_allowed_time = ConfigurationValueBool("boost_failed_card_allowed_time", "Boost failed card allowed time", True)

        def set_enable_fsrs_short_term_with_steps(toggle: bool) -> None:
            # noinspection PyProtectedMember, PyArgumentList
            mw.col._set_enable_fsrs_short_term_with_steps(toggle)

        self.autoadvance_vocab_starting_seconds = ConfigurationValueFloat("autoadvance_vocab_starting_seconds", "Starting Seconds", 3.0)
        self.autoadvance_vocab_hiragana_seconds = ConfigurationValueFloat("autoadvance_vocab_hiragana_seconds", "Hiragana Seconds", 0.7)
        self.autoadvance_vocab_katakana_seconds = ConfigurationValueFloat("autoadvance_vocab_katakana_seconds", "Katakana Seconds", 0.7)
        self.autoadvance_vocab_kanji_seconds = ConfigurationValueFloat("autoadvance_vocab_kanji_seconds", "Kanji Seconds", 1.5)

        self.autoadvance_sentence_starting_seconds = ConfigurationValueFloat("autoadvance_sentence_starting_seconds", "Starting Seconds", 3.0)
        self.autoadvance_sentence_hiragana_seconds = ConfigurationValueFloat("autoadvance_sentence_hiragana_seconds", "Hiragana Seconds", 0.7)
        self.autoadvance_sentence_katakana_seconds = ConfigurationValueFloat("autoadvance_sentence_katakana_seconds", "Katakana Seconds", 0.7)
        self.autoadvance_sentence_kanji_seconds = ConfigurationValueFloat("autoadvance_sentence_kanji_seconds", "Kanji Seconds", 1.5)

        self.timebox_vocab_read = ConfigurationValueInt("time_box_length_vocab_read", "Vocab Read", 15)
        self.timebox_vocab_listen = ConfigurationValueInt("time_box_length_vocab_listen", "Vocab Listen", 15)
        self.timebox_sentence_read = ConfigurationValueInt("time_box_length_sentence_read", "Sentence Read", 15)
        self.timebox_sentence_listen = ConfigurationValueInt("time_box_length_sentence_listen", "Sentence Listen", 15)
        self.timebox_kanji_read = ConfigurationValueInt("time_box_length_kanji", "Kanji", 15)
        self.yomitan_integration_copy_answer_to_clipboard = ConfigurationValueBool("yomitan_integration_copy_answer_to_clipboard", "Yomitan integration: Copy reviewer answer to clipboard", False)

        self.anki_internal_fsrs_set_enable_fsrs_short_term_with_steps = ConfigurationValueBool("fsrs_set_enable_fsrs_short_term_with_steps",
                                                                                               "FSRS: Enable short term scheduler with steps",
                                                                                               default=False,
                                                                                               feature_toggler=set_enable_fsrs_short_term_with_steps)

        self.decrease_failed_card_intervals = ConfigurationValueBool("decrease_failed_card_intervals", "Decrease failed card intervals", False)

        self.prevent_double_clicks = ConfigurationValueBool("prevent_double_clicks", "Prevent double clicks", True)
        self.prefer_default_mnemonics_to_source_mnemonics = ConfigurationValueBool("prefer_default_mnemocs_to_source_mnemonics", "Prefer default mnemonics to source mnemonics", False)

        self.enable_garbage_collection_during_batches = ConfigurationValueBool("enable_garbage_collection_during_batches", "Enable Batch GC. Requires restart. (Eliminates LARGE memory leak on sync, but slows down startup and batches and introduces short 'hangs'.", True)
        self.enable_automatic_garbage_collection = ConfigurationValueBool("enable_automatic_garbage_collection", "Enable automatic GC. Requires restart. (Reduces memory usage the most but slows Anki down and may cause crashes due to Qt incompatibility.", False)
        self.track_instances_in_memory = ConfigurationValueBool("track_instances_in_memory", "Track instances in memory. Requires restart. Only useful to developers and will use extra memory.", False)
        self.show_compound_parts_in_sentence_breakdown = ConfigurationValueBool("show_compound_parts_in_sentence_breakdown", "Show compound parts in sentence breakdown", True)
        self.show_all_matched_words_in_sentence_breakdown = ConfigurationValueBool("show_all_matched_words_in_sentence_breakdown", "Show all matched words in sentence breakdown", False)
        self.automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound = ConfigurationValueBool("automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound", "Automatically yield last token in suru verb compounds to overlapping compounds (Ctrl+Shift+Alt+s)", True)
        self.automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound = ConfigurationValueBool("automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound", "Automatically yield last token in passive verb compounds to overlapping compounds (Ctrl+Shift+Alt+h)", True)
        self.automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound = ConfigurationValueBool("automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound", "Automatically yield last token in causative verb compounds to overlapping compounds (Ctrl+Shift+Alt+t)", True)

        self.decrease_failed_card_intervals_interval = ConfigurationValueInt("decrease_failed_card_intervals_interval", "Failed card again seconds for next again", 60)

        self.minimum_time_viewing_question = ConfigurationValueFloat("minimum_time_viewing_question", "Minimum time viewing question", 0.5)
        self.minimum_time_viewing_answer = ConfigurationValueFloat("minimum_time_viewing_answer", "Minimum time viewing answer", 0.5)

        self.feature_toggles: list[tuple[str, list[ConfigurationValueBool]]] = \
            [("Sentence Display", [self.automatically_yield_last_token_in_suru_verb_compounds_to_overlapping_compound,
                                   self.automatically_yield_last_token_in_passive_verb_compounds_to_overlapping_compound,
                                   self.automatically_yield_last_token_in_causative_verb_compounds_to_overlapping_compound,
                                   self.show_compound_parts_in_sentence_breakdown,
                                   self.show_all_matched_words_in_sentence_breakdown]),
             ("Misc", [self.yomitan_integration_copy_answer_to_clipboard,
                       self.anki_internal_fsrs_set_enable_fsrs_short_term_with_steps,
                       self.decrease_failed_card_intervals,
                       self.prevent_double_clicks,
                       self.boost_failed_card_allowed_time,
                       self.prefer_default_mnemonics_to_source_mnemonics]),
             ("Memory", [self.enable_garbage_collection_during_batches,
                         self.enable_automatic_garbage_collection,
                         self.track_instances_in_memory])]

        self.readings_mappings_dict = self._read_reading_mappings_from_file()

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

    @classmethod
    def _read_reading_mappings_from_file(cls) -> dict[str, str]:
        return cls._parse_mappings_from_string(cls.read_readings_mappings_file())

    @staticmethod
    def _parse_mappings_from_string(mappings_string: str) -> dict[str, str]:
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

    @staticmethod
    def _mappings_file_path() -> str:
        return os.path.join(app.user_files_dir, "readings_mappings.txt")

config: Lazy[JapaneseConfig] = Lazy(lambda: JapaneseConfig())
