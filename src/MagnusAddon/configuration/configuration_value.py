from __future__ import annotations
from typing import Callable, Generic, Optional, TypeVar
import os
from aqt import mw

T = TypeVar('T')

_addon_dir = os.path.dirname(os.path.dirname(__file__))
_addon_name = os.path.basename(_addon_dir)

_config_dict = mw.addonManager.getConfig(_addon_name) or {}

class ConfigurationValue(Generic[T]):
    def __init__(self, name: str, title: str, default: T, feature_toggler: Optional[Callable[[T], None]] = None) -> None:
        self.title = title
        self.feature_toggler: Optional[Callable[[T], None]] = feature_toggler
        self.name = name
        self._value: T = _config_dict.get(name, default)

        if self.feature_toggler:
            from ankiutils import app
            app.add_init_hook(self.toggle_feature)

    def get_value(self) -> T:
        return self._value

    def set_value(self, value: T) -> None:
        self._value = value
        _config_dict[self.name] = value
        self.toggle_feature()
        mw.addonManager.writeConfig(_addon_name, _config_dict)

    def toggle_feature(self) -> None:
        if self.feature_toggler is not None:
            self.feature_toggler(self._value)

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

        self.decrease_failed_card_intervals_interval = ConfigurationValueInt("decrease_failed_card_intervals_interval", "Failed card again seconds for next again", 60)
        self.decrease_failed_card_intervals = ConfigurationValueBool("decrease_failed_card_intervals", "Decrease failed card intervals", False)

        self.prevent_double_clicks = ConfigurationValueBool("prevent_double_clicks", "Prevent double clicks", True)
        self.minimum_time_viewing_question = ConfigurationValueFloat("minimum_time_viewing_question", "Minimum time viewing question", 0.5)
        self.minimum_time_viewing_answer = ConfigurationValueFloat("minimum_time_viewing_answer", "Minimum time viewing answer", 0.5)

        self.feature_toggles = [self.yomitan_integration_copy_answer_to_clipboard, self.anki_internal_fsrs_set_enable_fsrs_short_term_with_steps, self.decrease_failed_card_intervals, self.prevent_double_clicks, self.boost_failed_card_allowed_time]


config = JapaneseConfig()
