from __future__ import annotations

from typing import TYPE_CHECKING, cast, final

from autoslot import Slots
from language_services.jamdict_ex import jmd_pos_map
from sysutils import kana_utils, typed
from typed_linq_collections.collections.q_list import QList
from typed_linq_collections.q_iterable import query

if TYPE_CHECKING:
    from collections.abc import Sequence

    from jamdict.jmdict import JMDEntry, Sense  # pyright: ignore[reportMissingTypeStubs]
    from typed_linq_collections.collections.q_set import QSet

class SenseEX(Slots):
    def __init__(self, source: Sense) -> None:
        self.gloss:QList[str] = query(source.gloss).select(lambda it: typed.str_(it.text)).to_list()  # pyright: ignore [reportUnknownArgumentType, reportUnknownMemberType]
        self.pos: QList[str] = QList(cast(list[str], source.pos))  # pyright: ignore [reportUnknownMemberType]
        self.is_kana_only = "word usually written using kana alone" in cast(list[str], source.misc) # pyright: ignore [reportUnknownMemberType]

    def is_transitive_verb(self) -> bool: return any(pos_item == "transitive verb" for pos_item in self.pos)
    def is_intransitive_verb(self) -> bool: return any(pos_item == "intransitive verb" for pos_item in self.pos)

@final
class DictEntry(Slots):
    def __init__(self, source: JMDEntry) -> None:
        self.kana_forms: QList[str] = query(source.kana_forms).select(lambda it: typed.str_(it.text)).to_list()  # pyright: ignore [reportUnknownMemberType, reportUnknownArgumentType]
        self.kanji_forms: QList[str] = query(source.kanji_forms).select(lambda it: typed.str_(it.text)).to_list()  # pyright: ignore [reportUnknownArgumentType, reportUnknownMemberType]
        self.senses: QList[SenseEX] = query(source.senses).select(SenseEX).to_list()

    def is_kana_only(self) -> bool:
        return not self.kanji_forms or self.senses.any(lambda sense: sense.is_kana_only)

    @staticmethod
    def create(entries: Sequence[JMDEntry]) -> QList[DictEntry]:
        return QList(DictEntry(entry) for entry in entries)

    def has_matching_kana_form(self, search: str) -> bool:
        search = kana_utils.katakana_to_hiragana(search)  # todo: this converting to hiragana is worrisome. Is this really the behavior we want? What false positives might we run into?
        return any(search == kana_utils.katakana_to_hiragana(form) for form in self.kana_forms)

    def has_matching_kanji_form(self, search: str) -> bool:
        search = kana_utils.katakana_to_hiragana(search)  # todo: this converting to hiragana is worrisome. Is this really the behavior we want? What false positives might we run into?
        return any(search == kana_utils.katakana_to_hiragana(form) for form in self.kanji_forms)

    def valid_forms(self, force_allow_kana_only: bool = False) -> QSet[str]:
        return self.kana_forms.to_set() | self.kanji_forms.to_set() if self.is_kana_only() or force_allow_kana_only else self.kanji_forms.to_set()

    def _is_transitive_verb(self) -> bool:
        return self.senses.all(lambda it: it.is_transitive_verb())

    def _is_intransitive_verb(self) -> bool:
        return self.senses.all(lambda it: it.is_intransitive_verb())

    def _is_verb(self) -> bool:
        return (any(sense.is_intransitive_verb() for sense in self.senses)
                or any(sense.is_transitive_verb() for sense in self.senses)
                or any(" verb " in s.pos[0] for s in self.senses if len(s.pos) > 0))

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

        return (query(self.senses)
                .select_many(lambda sense: sense.gloss)
                .all(lambda gloss: gloss.startswith("to be ")))

    def format_sense(self, sense: SenseEX) -> str:
        glosses_text = sense.gloss
        glosses_text = [gloss.replace(" ", "-") for gloss in glosses_text]
        if self._is_verb():
            if all(gloss[:6] == "to-be-" for gloss in glosses_text):  # noqa: SIM108
                glosses_text = [gloss[6:] for gloss in glosses_text]
            else:
                glosses_text = [gloss[3:] if gloss[:3] == "to-" else gloss for gloss in glosses_text]
        return "/".join(glosses_text)

    def generate_answer(self) -> str:
        prefix = self._answer_prefix()
        senses = list(self.senses)
        formatted_senses = [self.format_sense(sense) for sense in senses]
        return prefix + " | ".join(formatted_senses)

    def parts_of_speech(self) -> QSet[str]:
        return (query(self.senses)
                .select_many(lambda sense: sense.pos)
                .select_many(jmd_pos_map.try_get_our_pos_name)
                .to_set())