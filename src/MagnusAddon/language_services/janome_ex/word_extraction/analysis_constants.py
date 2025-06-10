from __future__ import annotations

from sysutils import ex_str

noise_characters = {".", ",", ":", ";", "/", "|", "。", "、", "?", "!", "～", "｡", ex_str.invisible_space}
non_word_characters = noise_characters | {" ", "\t"}
