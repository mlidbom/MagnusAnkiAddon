from __future__ import annotations

import os
from typing import Callable, Generic, Optional, TypeVar

from ankiutils import app
from aqt import mw
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
        self._update_callbacks: list[Callable[[], None]] = []

        if self.feature_toggler:
            app.add_init_hook(self.toggle_feature)

    def get_value(self) -> T:
        return self._value

    def set_value(self, value: T) -> None:
        self._value = value
        _config_dict.instance()[self.name] = value
        self.toggle_feature()
        for callback in self._update_callbacks: callback()
        _write_config_dict()

    def toggle_feature(self) -> None:
        if self.feature_toggler is not None:
            self.feature_toggler(self._value)

    def register_update_callback(self, callback: Callable[[], None]) -> None:
        self._update_callbacks.append(callback)

ConfigurationValueInt = ConfigurationValue[int]
ConfigurationValueFloat = ConfigurationValue[float]
ConfigurationValueBool = ConfigurationValue[bool]
ConfigurationValueString = ConfigurationValue[str]

class JapaneseConfig:
    def __init__(self) -> None:
        self.boost_failed_card_allowed_time_by_factor = ConfigurationValueFloat("boost_failed_card_allowed_time_by_factor", "Boost Failed Card Allowed Time Factor", 1.5)
        self.boost_failed_card_allowed_time = ConfigurationValueBool("boost_failed_card_allowed_time", "Boost failed card allowed time", True)

        def set_enable_fsrs_short_term_with_steps(toggle: bool) -> None:
            # noinspection PyProtectedMember, PyArgumentList
            mw.col._set_enable_fsrs_short_term_with_steps(toggle)

        self.readings_mappings = ConfigurationValueString("readings_mappings", "Readings Mappings", "")

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
        self.prefer_default_mnemocs_to_source_mnemonics = ConfigurationValueBool("prefer_default_mnemocs_to_source_mnemonics", "Prefer default mnemonics to source mnemonics", False)
        self.enable_garbage_collection = ConfigurationValueBool("enable_garbage_collection", "Enable GC. Requires restart. (Reduces memory usage but slows Anki down and may cause crashes due to Qt incompatibility.", False)


        self.decrease_failed_card_intervals_interval = ConfigurationValueInt("decrease_failed_card_intervals_interval", "Failed card again seconds for next again", 60)


        self.minimum_time_viewing_question = ConfigurationValueFloat("minimum_time_viewing_question", "Minimum time viewing question", 0.5)
        self.minimum_time_viewing_answer = ConfigurationValueFloat("minimum_time_viewing_answer", "Minimum time viewing answer", 0.5)

        self.feature_toggles = [self.yomitan_integration_copy_answer_to_clipboard,
                                self.anki_internal_fsrs_set_enable_fsrs_short_term_with_steps,
                                self.decrease_failed_card_intervals,
                                self.prevent_double_clicks,
                                self.boost_failed_card_allowed_time,
                                self.prefer_default_mnemocs_to_source_mnemonics,
                                self.enable_garbage_collection]

        self.readings_mappings_dict = self.get_readings_mappings()
        self.readings_mappings.register_update_callback(self._update_after_save)

    def _update_after_save(self) -> None:
        self.readings_mappings_dict = self.get_readings_mappings()

    def get_readings_mappings(self) -> dict[str, str]:
        def parse_value_part(value_part: str) -> str:
            if "<read>" in value_part:
                return value_part
            if ":" in value_part:
                parts = value_part.split(":", 1)
                return f"""<read>{parts[0].strip()}</read>{parts[1]}"""
            return f"<read>{value_part}</read>"


        readings_mappings = {
            line.split(":", 1)[0].strip(): parse_value_part(line.split(":", 1)[1].strip())
            for line in self.readings_mappings.get_value().strip().splitlines()
            if ":" in line
        }

        return readings_mappings






config:Lazy[JapaneseConfig] = Lazy(lambda: JapaneseConfig())
