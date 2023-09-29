from typing import Sequence

from jamdict.jmdict import JMDEntry, Sense

from sysutils import kana_utils
from sysutils.listutils import ListUtils


class DictEntry:
    def __init__(self, entry: JMDEntry) -> None:
        self.entry = entry

    def is_kana_only(self) -> bool:
        return not self.entry.kanji_forms or any((sense for sense
                                                  in self.entry.senses
                                                  if 'word usually written using kana alone' in sense.misc))

    @classmethod
    def create(cls, entries: Sequence[JMDEntry]) -> list['DictEntry']:
        return [cls(entry) for entry in entries]

    def has_matching_kana_form(self, search: str) -> bool:
        search = kana_utils.to_hiragana(search)
        return any(search == kana_utils.to_hiragana(form) for form in self.kana_forms())

    def is_default_kana_form(self, search: str) -> bool:
        search = kana_utils.to_hiragana(search)
        return search == kana_utils.to_hiragana(self.kana_forms()[0])

    def has_matching_kanji_form(self, search: str) -> bool:
        search = kana_utils.to_hiragana(search)
        return any(search == kana_utils.to_hiragana(form) for form in self.kanji_forms())

    def is_default_kanji_form(self, search: str) -> bool:
        search = kana_utils.to_hiragana(search)
        return search == kana_utils.to_hiragana(self.kanji_forms()[0])

    def kana_forms(self) -> list[str]: return [ent.text for ent in self.entry.kana_forms]
    def kanji_forms(self) -> list[str]: return [ent.text for ent in self.entry.kanji_forms]
    def valid_forms(self, force_allow_kana_only: bool = False) -> set[str]:
        return set(self.kana_forms()) | set(self.kanji_forms()) if self.is_kana_only() or force_allow_kana_only else self.kanji_forms()

    def _is_verb(self) -> bool:
        return any("verb" in s.pos[0] for s in self.entry.senses)

    def _answer_prefix(self) -> str:
        if self._is_verb():
            return "to? be: " if self._is_to_be_verb() else "to? "
        return ""

    def _is_to_be_verb(self) -> bool:
        if not self._is_verb():
            return False

        glosses_text:list[str] = ListUtils.flatten_list([[str(gloss.text) for gloss in sense.gloss] for sense in self.entry.senses])
        return all(gloss.startswith("to be ") for gloss in glosses_text)

    def format_sense(self, sense:Sense) -> str:
        glosses_text = [str(gloss.text) for gloss in sense.gloss]
        glosses_text = [gloss.replace(" ", "-") for gloss in glosses_text]
        if self._is_verb():
            if all(gloss[:6] == "to-be-" for gloss in glosses_text):
                glosses_text = [gloss[6:] for gloss in glosses_text]
            else:
                glosses_text = [gloss[3:] if gloss[:3] == "to-" else gloss for gloss in glosses_text]
        sense_text = "/".join(glosses_text)
        return sense_text

    def generate_answer(self) -> str:
        prefix = self._answer_prefix()
        senses = [sense for sense in self.entry.senses]
        formatted_senses = [self.format_sense(sense) for sense in senses]
        answer_text = prefix + " | ".join(formatted_senses)
        return answer_text
