from __future__ import annotations

from typing import TYPE_CHECKING

from sysutils import ex_sequence, kana_utils

if TYPE_CHECKING:
    from collections.abc import Sequence

    from jamdict.jmdict import JMDEntry, Sense


def _sense_is_transitive_verb(sense: Sense) -> bool:
    return any(pos_item == "transitive verb" for pos_item in sense.pos)

def _sense_is_intransitive_verb(sense: Sense) -> bool:
    return any(pos_item == "intransitive verb" for pos_item in sense.pos)

class DictEntry:
    def __init__(self, entry: JMDEntry, lookup_word: str, lookup_readings: list[str]) -> None:
        self.entry = entry
        self.lookup_word = lookup_word
        self.lookup_readings = lookup_readings

    def is_kana_only(self) -> bool:
        return not self.entry.kanji_forms or any(sense for sense
                                                 in self.entry.senses
                                                 if "word usually written using kana alone" in sense.misc)

    @classmethod
    def create(cls, entries: Sequence[JMDEntry], lookup_word: str, lookup_reading: list[str]) -> list[DictEntry]:
        return [cls(entry, lookup_word, lookup_reading) for entry in entries]

    def has_matching_kana_form(self, search: str) -> bool:
        search = kana_utils.katakana_to_hiragana(search)  # todo: this converting to hiragana is worrisome. Is this really the behavior we want? What false positives might we run into?
        return any(search == kana_utils.katakana_to_hiragana(form) for form in self.kana_forms())

    def has_matching_kanji_form(self, search: str) -> bool:
        search = kana_utils.katakana_to_hiragana(search)  # todo: this converting to hiragana is worrisome. Is this really the behavior we want? What false positives might we run into?
        return any(search == kana_utils.katakana_to_hiragana(form) for form in self.kanji_forms())

    def kana_forms(self) -> list[str]: return [ent.text for ent in self.entry.kana_forms]
    def kanji_forms(self) -> list[str]: return [ent.text for ent in self.entry.kanji_forms]
    def valid_forms(self, force_allow_kana_only: bool = False) -> set[str]:
        return set(self.kana_forms()) | set(self.kanji_forms()) if self.is_kana_only() or force_allow_kana_only else set(self.kanji_forms())

    def priority_tags(self) -> set[str]:
        kanji_priorities: list[str] = ex_sequence.flatten([form.pri for form in self.entry.kanji_forms if form.text == self.lookup_word])
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

        glosses_text: list[str] = ex_sequence.flatten([[str(gloss.text) for gloss in sense.gloss] for sense in self.entry.senses])
        return all(gloss.startswith("to be ") for gloss in glosses_text)

    def format_sense(self, sense: Sense) -> str:
        glosses_text = [str(gloss.text) for gloss in sense.gloss]
        glosses_text = [gloss.replace(" ", "-") for gloss in glosses_text]
        if self._is_verb():
            if all(gloss[:6] == "to-be-" for gloss in glosses_text):  # noqa: SIM108
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
        "pre-noun adjectival (rentaishi)": [""],
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
        def try_get_pos(pos: str) -> list[str]:
            return self._parts_of_speech_map[pos] if pos in self._parts_of_speech_map else ["unmapped-pos-" + pos]

        return set(ex_sequence.flatten([ex_sequence.flatten([try_get_pos(pos) for pos in sense.pos]) for sense in self.entry.senses]))
