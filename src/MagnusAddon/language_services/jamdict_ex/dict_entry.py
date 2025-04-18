from typing import Sequence

from jamdict.jmdict import JMDEntry, Sense

from sysutils import kana_utils
from sysutils import ex_sequence

def _sense_is_transitive_verb(sense: Sense) -> bool:
    return any("transitive verb" == pos_item for pos_item in sense.pos)

def _sense_is_intransitive_verb(sense: Sense) -> bool:
    return any("intransitive verb" == pos_item for pos_item in sense.pos)

class DictEntry:
    def __init__(self, entry: JMDEntry, lookup_word: str, lookup_readings: list[str]) -> None:
        self.entry = entry
        self.lookup_word = lookup_word
        self.lookup_readings = lookup_readings

    def is_kana_only(self) -> bool:
        return not self.entry.kanji_forms or any((sense for sense
                                                  in self.entry.senses
                                                  if 'word usually written using kana alone' in sense.misc))

    @classmethod
    def create(cls, entries: Sequence[JMDEntry], lookup_word: str, lookup_reading: list[str]) -> list['DictEntry']:
        return [cls(entry, lookup_word, lookup_reading) for entry in entries]

    def has_matching_kana_form(self, search: str) -> bool:
        search = kana_utils.to_hiragana(search) # todo: this converting to hiragana is worrisome. Is this really the behavior we want? What false positives might we run into?
        return any(search == kana_utils.to_hiragana(form) for form in self.kana_forms())

    def has_matching_kanji_form(self, search: str) -> bool:
        search = kana_utils.to_hiragana(search) # todo: this converting to hiragana is worrisome. Is this really the behavior we want? What false positives might we run into?
        return any(search == kana_utils.to_hiragana(form) for form in self.kanji_forms())

    def kana_forms(self) -> list[str]: return [ent.text for ent in self.entry.kana_forms]
    def kanji_forms(self) -> list[str]: return [ent.text for ent in self.entry.kanji_forms]
    def valid_forms(self, force_allow_kana_only: bool = False) -> set[str]:
        return set(self.kana_forms()) | set(self.kanji_forms()) if self.is_kana_only() or force_allow_kana_only else set(self.kanji_forms())

    def priority_tags(self) -> set[str]:
        kanji_priorities:list[str] = ex_sequence.flatten([form.pri for form in self.entry.kanji_forms if form.text == self.lookup_word])
        kana_priorities: list[str] = ex_sequence.flatten([form.pri for form in self.entry.kana_forms if form.text in self.lookup_readings])

        tags = set(kanji_priorities + kana_priorities)

        return tags



    def _is_transitive_verb(self) -> bool:
        return all(_sense_is_transitive_verb(sense) for sense in self.entry.senses)

    def _is_intransitive_verb(self) -> bool:
        return all(_sense_is_intransitive_verb(sense) for sense in self.entry.senses)

    def _is_verb(self) -> bool:
        return (any(_sense_is_intransitive_verb(sense) for sense in self.entry.senses)
                or any(_sense_is_transitive_verb(sense) for sense in self.entry.senses)
                or any(" verb " in s.pos[0] for s in self.entry.senses))

    def _answer_prefix(self) -> str:
        if self._is_verb():
            if self._is_intransitive_verb():
                return "to: "
            if self._is_transitive_verb():
                return "to{} "
            if self._is_to_be_verb():
                return "to: be: "

            return "to? "

        return ""

    def _is_to_be_verb(self) -> bool:
        if not self._is_verb():
            return False

        glosses_text:list[str] = ex_sequence.flatten([[str(gloss.text) for gloss in sense.gloss] for sense in self.entry.senses])
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
