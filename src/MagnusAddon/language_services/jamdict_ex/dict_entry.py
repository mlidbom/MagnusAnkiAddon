from __future__ import annotations

from typing import TYPE_CHECKING, cast, final

from autoslot import Slots
from note.vocabulary.pos_set_interner import POSSetManager
from sysutils import kana_utils
from typed_linq_collections.collections.q_list import QList
from typed_linq_collections.q_iterable import query

if TYPE_CHECKING:
    from collections.abc import Sequence

    from jamdict.jmdict import JMDEntry, KanaForm, KanjiForm, Sense  # pyright: ignore[reportMissingTypeStubs]
    from typed_linq_collections.collections.q_set import QSet

class SenseEX(Slots):
    def __init__(self, source: Sense) -> None:
        self.glosses: QList[str] = query(source.gloss).select(lambda it: cast(str, it.text).replace(" ", "-")).to_list()  # pyright: ignore [reportUnknownArgumentType, reportUnknownMemberType]
        # POSSetManager handles JMDict -> our names mapping and interning
        self.pos: frozenset[str] = POSSetManager.intern_and_harmonize_from_list(cast(list[str], source.pos))  # pyright: ignore [reportUnknownMemberType]
        self.is_kana_only: bool = "word usually written using kana alone" in cast(list[str], source.misc)  # pyright: ignore [reportUnknownMemberType]

    def is_transitive_verb(self) -> bool: return POSSetManager.is_transitive_verb(self.pos)
    def is_intransitive_verb(self) -> bool: return POSSetManager.is_intransitive_verb(self.pos)

    def _all_glosses_start_with(self, prefix: str) -> bool: return self.glosses.all(lambda it: it.startswith(prefix))

    def format_glosses(self) -> str:
        if POSSetManager.is_verb(self.pos):
            type_marker = "{?}"
            if self.is_transitive_verb(): type_marker = "{}"
            if self.is_intransitive_verb(): type_marker = ":"

            start_group = "{"
            end_group = "}"
            if len(self.glosses) == 1:
                start_group = ""
                end_group = ""

            if self._all_glosses_start_with("to-be-"):
                return f"""to-be{type_marker}{start_group}{"/".join(self.glosses.select(lambda it: it.removeprefix("to-be-")))}{end_group}"""

            if self._all_glosses_start_with("to-"):
                return f"""to{type_marker}{start_group}{"/".join(self.glosses.select(lambda it: it.removeprefix("to-")))}{end_group}"""

        return "/".join(self.glosses)

class KanaFormEX(Slots):
    def __init__(self, source: KanaForm) -> None:
        self.text: str = source.text  # pyright: ignore [reportUnknownMemberType]
        self.priority_tags: QList[str] = QList(cast(list[str], source.pri))  # pyright: ignore [reportUnknownMemberType]

class KanjiFormEX(Slots):
    def __init__(self, source: KanjiForm) -> None:
        self.text: str = source.text  # pyright: ignore [reportUnknownMemberType]
        self.priority_tags: QList[str] = QList(cast(list[str], source.pri))  # pyright: ignore [reportUnknownMemberType]

@final
class DictEntry(Slots):
    def __init__(self, source: JMDEntry) -> None:
        self.kana_forms: QList[KanaFormEX] = query(source.kana_forms).select(KanaFormEX).to_list()
        self.kanji_forms: QList[KanjiFormEX] = query(source.kanji_forms).select(KanjiFormEX).to_list()
        self.senses: QList[SenseEX] = query(source.senses).select(SenseEX).to_list()

    def kana_forms_text(self) -> QList[str]: return self.kana_forms.select(lambda it: it.text).to_list()
    def kanji_forms_text(self) -> QList[str]: return self.kanji_forms.select(lambda it: it.text).to_list()

    def is_kana_only(self) -> bool:
        return not self.kanji_forms or self.senses.any(lambda sense: sense.is_kana_only)

    @classmethod
    def create(cls, entries: Sequence[JMDEntry]) -> QList[DictEntry]:
        return QList(DictEntry(entry) for entry in entries)

    def has_matching_kana_form(self, search: str) -> bool:
        search = kana_utils.katakana_to_hiragana(search)  # todo: this converting to hiragana is worrisome. Is this really the behavior we want? What false positives might we run into?
        return any(search == kana_utils.katakana_to_hiragana(form.text) for form in self.kana_forms)

    def has_matching_kanji_form(self, search: str) -> bool:
        search = kana_utils.katakana_to_hiragana(search)  # todo: this converting to hiragana is worrisome. Is this really the behavior we want? What false positives might we run into?
        return any(search == kana_utils.katakana_to_hiragana(form.text) for form in self.kanji_forms)

    def valid_forms(self, force_allow_kana_only: bool = False) -> QSet[str]:
        return self.kana_forms_text().to_set() | self.kanji_forms_text().to_set() if self.is_kana_only() or force_allow_kana_only else self.kanji_forms_text().to_set()

    def is_transitive_verb(self) -> bool:
        return self.senses.all(lambda it: it.is_transitive_verb())

    def is_intransitive_verb(self) -> bool:
        return self.senses.all(lambda it: it.is_intransitive_verb())

    def format_answer(self) -> str:
        def default_senses_format() -> str:
            return " | ".join(self.senses.select(lambda it: it.format_glosses()))

        return default_senses_format()

    def parts_of_speech(self) -> QSet[str]:
        # POS values are already mapped and harmonized in SenseEX
        return (query(self.senses)
                .select_many(lambda sense: sense.pos)
                .to_set())
