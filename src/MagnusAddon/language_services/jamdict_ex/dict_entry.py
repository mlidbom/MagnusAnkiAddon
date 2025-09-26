from __future__ import annotations

from typing import TYPE_CHECKING, final

from ex_autoslot import AutoSlots
from typed_linq_collections.collections.q_list import QList
from typed_linq_collections.q_iterable import query
from sysutils import kana_utils
from sysutils.typed import checked_cast_generics, str_

if TYPE_CHECKING:
    from collections.abc import Sequence

    from jamdict.jmdict import JMDEntry, Sense  # pyright: ignore[reportMissingTypeStubs]

def _sense_is_transitive_verb(sense: Sense) -> bool:
    return any(pos_item == "transitive verb" for pos_item in sense.pos)  # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType, reportUnknownMemberType]

def _sense_is_intransitive_verb(sense: Sense) -> bool:
    return any(pos_item == "intransitive verb" for pos_item in sense.pos)  # pyright: ignore[reportUnknownVariableType, reportUnknownArgumentType, reportUnknownMemberType]

@final
class DictEntry(AutoSlots):
    def __init__(self, entry: JMDEntry, lookup_word: str, lookup_readings: list[str]) -> None:
        self.entry: JMDEntry = entry
        self.lookup_word: str = lookup_word
        self.lookup_readings: list[str] = lookup_readings

    def is_kana_only(self) -> bool:
        return not self.entry.kanji_forms or any(sense for sense
                                                 in self.entry.senses
                                                 if "word usually written using kana alone" in sense.misc)  # pyright: ignore[reportUnknownMemberType]

    @staticmethod
    def create(entries: Sequence[JMDEntry], lookup_word: str, lookup_reading: list[str]) -> QList[DictEntry]:
        return QList(DictEntry(entry, lookup_word, lookup_reading) for entry in entries)

    def has_matching_kana_form(self, search: str) -> bool:
        search = kana_utils.katakana_to_hiragana(search)  # todo: this converting to hiragana is worrisome. Is this really the behavior we want? What false positives might we run into?
        return any(search == kana_utils.katakana_to_hiragana(form) for form in self.kana_forms())

    def has_matching_kanji_form(self, search: str) -> bool:
        search = kana_utils.katakana_to_hiragana(search)  # todo: this converting to hiragana is worrisome. Is this really the behavior we want? What false positives might we run into?
        return any(search == kana_utils.katakana_to_hiragana(form) for form in self.kanji_forms())

    def kana_forms(self) -> list[str]: return [ent.text for ent in self.entry.kana_forms]  # pyright: ignore[reportUnknownMemberType]
    def kanji_forms(self) -> list[str]: return [ent.text for ent in self.entry.kanji_forms]  # pyright: ignore[reportUnknownMemberType]
    def valid_forms(self, force_allow_kana_only: bool = False) -> set[str]:
        return set(self.kana_forms()) | set(self.kanji_forms()) if self.is_kana_only() or force_allow_kana_only else set(self.kanji_forms())

    def priority_tags(self) -> set[str]:
        kanji_priorities: QList[str] = (query(self.entry.kanji_forms)
                                        .where(lambda form: str_(form.text) == self.lookup_word)  # pyright: ignore [reportUnknownArgumentType, reportUnknownMemberType]
                                        .select_many(lambda form: checked_cast_generics(list[str], form.pri))  # pyright: ignore [reportUnknownArgumentType, reportUnknownMemberType]
                                        .to_list())
        kana_priorities: list[str] = (query(self.entry.kana_forms)
                                      .where(lambda form: str_(form.text) in self.lookup_readings)  # pyright: ignore [reportUnknownArgumentType, reportUnknownMemberType]
                                      .select_many(lambda form: checked_cast_generics(list[str], form.pri))  # pyright: ignore [reportUnknownArgumentType, reportUnknownMemberType]
                                      .to_list())  # ex_sequence.flatten([str_(form.pri) for form in self.entry.kana_forms if str_(form.text) in self.lookup_readings])  # pyright: ignore [reportUnknownArgumentType, reportUnknownMemberType]

        return set(kanji_priorities + kana_priorities)

    def _is_transitive_verb(self) -> bool:
        return all(_sense_is_transitive_verb(sense) for sense in self.entry.senses)

    def _is_intransitive_verb(self) -> bool:
        return all(_sense_is_intransitive_verb(sense) for sense in self.entry.senses)

    def _is_verb(self) -> bool:
        return (any(_sense_is_intransitive_verb(sense) for sense in self.entry.senses)
                or any(_sense_is_transitive_verb(sense) for sense in self.entry.senses)
                or any(" verb " in s.pos[0] for s in self.entry.senses if len(s.pos) > 0))  # pyright: ignore[reportUnknownArgumentType, reportUnknownMemberType]

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

        return (query(self.entry.senses)
                .select_many(lambda sense: sense.gloss)
                .select(lambda gloss: str_(gloss.text))  # pyright: ignore [reportUnknownArgumentType, reportUnknownMemberType]
                .all(lambda gloss: gloss.startswith("to be ")))

    def format_sense(self, sense: Sense) -> str:
        glosses_text = [str(gloss.text) for gloss in sense.gloss]  # pyright: ignore[reportUnknownArgumentType]
        glosses_text = [gloss.replace(" ", "-") for gloss in glosses_text]
        if self._is_verb():
            if all(gloss[:6] == "to-be-" for gloss in glosses_text):  # noqa: SIM108
                glosses_text = [gloss[6:] for gloss in glosses_text]
            else:
                glosses_text = [gloss[3:] if gloss[:3] == "to-" else gloss for gloss in glosses_text]
        return "/".join(glosses_text)

    def generate_answer(self) -> str:
        prefix = self._answer_prefix()
        senses = list(self.entry.senses)
        formatted_senses = [self.format_sense(sense) for sense in senses]
        return prefix + " | ".join(formatted_senses)

    _parts_of_speech_map = {
        "transitive verb": ["transitive"],
        "intransitive verb": ["intransitive"],
        "noun or participle which takes the aux. verb suru": ["suru verb"],
        "noun (common) (futsuumeishi)": ["noun"],
        "adjectival nouns or quasi-adjectives (keiyodoshi)": ["na-adjective"],
        "noun, used as a suffix": ["noun", "suffix"],
        "Godan verb with 'u' ending": ["godan verb"],
        "Godan verb with 'ru' ending": ["godan verb"],
        "Godan verb with 'mu' ending": ["godan verb"],
        "Godan verb with 'nu' ending": ["godan verb"],
        "Godan verb with 'gu' ending": ["godan verb"],
        "Godan verb with 'ku' ending": ["godan verb"],
        "Godan verb with 'su' ending": ["godan verb"],
        "Godan verb with 'bu' ending": ["godan verb"],
        "Godan verb with 'u' ending (special class)": ["godan verb", "special-class"],
        "Godan verb - -aru special class": ["godan verb", "special-class-aru"],
        "Godan verb with 'tsu' ending": ["godan verb"],
        "irregular nu verb": ["nu verb"],
        "Godan verb - Iku/Yuku special class": ["godan verb", "special-class"],
        "Godan verb with 'ru' ending (irregular verb)": ["godan verb", "irregular"],
        "Ichidan verb": ["ichidan verb"],
        "Ichidan verb - zuru verb (alternative form of -jiru verbs)": ["ichidan verb", "zuru verb"],
        "Kuru verb - special class": ["kuru verb", "special-class"],
        "Yodan verb with 'ru' ending (archaic)": ["yodan verb"],
        "Yodan verb with 'ku' ending (archaic)": ["yodan verb"],
        "Nidan verb (lower class) with 'ru' ending (archaic)": ["nidan verb"],
        "Nidan verb (upper class) with 'ru' ending (archaic)": ["nidan verb"],
        "adjective (keiyoushi)": ["i-adjective"],
        "adjective (keiyoushi) - yoi/ii class": ["i-adjective"],
        "adverb (fukushi)": ["adverb"],
        "adverb taking the 'to' particle": ["to-adverb"],
        "auxiliary": ["auxiliary"],
        "auxiliary adjective": ["adjective", "auxiliary"],
        "auxiliary verb": ["auxiliary"],
        "conjunction": ["conjunction"],
        "copula": ["copula"],
        "expressions (phrases, clauses, etc.)": ["expression"],
        "interjection (kandoushi)": ["interjection"],
        "irregular ru verb, plain form ends with -ri": [""],
        "noun, used as a prefix": ["prefix", "noun"],
        "nouns which may take the genitive case particle 'no'": ["noun", "no-adjective"],
        "particle": ["particle"],
        "pre-noun adjectival (rentaishi)": ["pre-noun-adjectival"],
        "prefix": ["prefix"],
        "pronoun": ["pronoun"],
        "suffix": ["suffix"],
        "suru verb - included": ["suru verb"],
        "suru verb": ["suru verb"],
        "su verb - precursor to the modern suru": ["su verb"],
        "counter": ["counter"],
        "numeric": ["numeric"],
        "noun or verb acting prenominally": ["prenominal"],
        "suru verb - special class": ["suru verb", "special-class"],
        "Ichidan verb - kureru special class": ["ichidan verb", "special-class"],
        "'taru' adjective": ["taru-adjective"]

    }
    def parts_of_speech(self) -> set[str]:
        def try_get_our_pos_name(pos: str) -> list[str]:
            return self._parts_of_speech_map[pos] if pos in self._parts_of_speech_map else ["unmapped-pos-" + pos]

        return (query(self.entry.senses)
                .select_many(lambda sense: checked_cast_generics(list[str], sense.pos))  # pyright: ignore [reportUnknownArgumentType, reportUnknownMemberType]
                .select_many(try_get_our_pos_name)
                .to_set())
