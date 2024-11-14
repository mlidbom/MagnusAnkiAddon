from typing import Any, Generic, TypeVar
from aqt import mw
import os

T = TypeVar('T', int, str, bool)

_addon_dir = os.path.dirname(os.path.dirname(__file__))
_addon_name = os.path.basename(_addon_dir)

_config_dict = mw.addonManager.getConfig(_addon_name) or {}

class JapaneseConfig:
    def __init__(self) -> None:
        self.timebox_vocab_read = ConfigurationValueInt("time_box_length_vocab_read", "Vocab Read", 15)
        self.timebox_vocab_listen = ConfigurationValueInt("time_box_length_vocab_listen", "Vocab Listen", 15)
        self.timebox_sentence_read = ConfigurationValueInt("time_box_length_sentence_read", "Sentence Read", 15)
        self.timebox_sentence_listen = ConfigurationValueInt("time_box_length_sentence_listen", "Sentence Listen", 15)
        self.timebox_kanji_read = ConfigurationValueInt("time_box_length_kanji", "Kanji", 15)
        self.yomitan_integration_copy_answer_to_clipboard = ConfigurationValueBool("yomitan_integration_copy_answer_to_clipboard", "Yomitan integration: Copy reviewer answer to clipboard", False)


class ConfigurationValue(Generic[T]):
    def __init__(self, name: str, title: str, default: T) -> None:
        self.title = title
        self.name = name
        self.value: T = _config_dict.get(name, default)

    def get_value(self) -> T:
        return self.value

    def set_value(self, value: T) -> None:
        self.value = value
        _config_dict[self.name] = value
        mw.addonManager.writeConfig(_addon_name, _config_dict)

# Type aliases for clarity
ConfigurationValueInt = ConfigurationValue[int]
ConfigurationValueStr = ConfigurationValue[str]
ConfigurationValueBool = ConfigurationValue[bool]
