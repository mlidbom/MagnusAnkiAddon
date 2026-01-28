from __future__ import annotations

from note.vocabulary.pos import POS
from sysutils import ex_str
from sysutils.memory_usage import string_auto_interner


class POSSetManager:
    _pos_by_str: dict[str, frozenset[str]] = {}

    #todo: I'm far from sure about the mapping that go from one to two, are we not losing information?
    _remappings: dict[str, list[str]] = {
        # Our own harmonizations (for VocabNote usage)
        "intransitive verb": [POS.INTRANSITIVE],
        "transitive verb": [POS.TRANSITIVE],
        "godan": [POS.GODAN_VERB],
        "ichidan": [POS.ICHIDAN_VERB],

        # JMDict POS mappings
        "な adjective": [POS.NA_ADJECTIVE],
        "noun or participle which takes the aux. verb suru": [POS.SURU_VERB],
        "noun (common) (futsuumeishi)": [POS.NOUN],
        "adjectival nouns or quasi-adjectives (keiyodoshi)": [POS.NA_ADJECTIVE],
        "noun, used as a suffix": [POS.NOUN, POS.SUFFIX],
        "godan verb with 'u' ending": [POS.GODAN_VERB],
        "godan verb with 'ru' ending": [POS.GODAN_VERB],
        "godan verb with 'mu' ending": [POS.GODAN_VERB],
        "godan verb with 'nu' ending": [POS.GODAN_VERB],
        "godan verb with 'gu' ending": [POS.GODAN_VERB],
        "godan verb with 'ku' ending": [POS.GODAN_VERB],
        "godan verb with 'su' ending": [POS.GODAN_VERB],
        "godan verb with 'bu' ending": [POS.GODAN_VERB],
        "godan verb with 'u' ending (special class)": [POS.GODAN_VERB, POS.SPECIAL_CLASS],
        "godan verb - -aru special class": [POS.GODAN_VERB, POS.SPECIAL_CLASS_ARU],
        "godan verb with 'tsu' ending": [POS.GODAN_VERB],
        "irregular nu verb": [POS.NU_VERB],
        "godan verb - iku/yuku special class": [POS.GODAN_VERB, POS.SPECIAL_CLASS],
        "godan verb with 'ru' ending (irregular verb)": [POS.GODAN_VERB, POS.IRREGULAR],
        "ichidan verb": [POS.ICHIDAN_VERB],
        "ichidan verb - zuru verb (alternative form of -jiru verbs)": [POS.ICHIDAN_VERB, POS.ZURU_VERB],
        "kuru verb - special class": [POS.KURU_VERB, POS.SPECIAL_CLASS],
        "yodan verb with 'ru' ending (archaic)": [POS.YODAN_VERB],
        "yodan verb with 'ku' ending (archaic)": [POS.YODAN_VERB],
        "nidan verb (lower class) with 'ru' ending (archaic)": [POS.NIDAN_VERB],
        "nidan verb (upper class) with 'ru' ending (archaic)": [POS.NIDAN_VERB],
        "adjective (keiyoushi)": [POS.I_ADJECTIVE],
        "adjective (keiyoushi) - yoi/ii class": [POS.I_ADJECTIVE],
        "adverb (fukushi)": [POS.ADVERB],
        "adverb taking the 'to' particle": [POS.TO_ADVERB],
        POS.AUXILIARY: [POS.AUXILIARY],
        "auxiliary adjective": [POS.I_ADJECTIVE, POS.AUXILIARY],
        "auxiliary verb": [POS.AUXILIARY],
        POS.CONJUNCTION: [POS.CONJUNCTION],
        POS.COPULA: [POS.COPULA],
        "expressions (phrases, clauses, etc.)": [POS.EXPRESSION],
        "interjection (kandoushi)": [POS.INTERJECTION],
        "noun, used as a prefix": [POS.PREFIX, POS.NOUN],
        "nouns which may take the genitive case particle 'no'": [POS.NOUN, POS.NO_ADJECTIVE],
        POS.PARTICLE: [POS.PARTICLE],
        "pre-noun adjectival (rentaishi)": [POS.PRE_NOUN_ADJECTIVAL],
        POS.PREFIX: [POS.PREFIX],
        POS.PRONOUN: [POS.PRONOUN],
        POS.SUFFIX: [POS.SUFFIX],
        "suru verb - included": [POS.SURU_VERB],
        POS.SURU_VERB: [POS.SURU_VERB],
        "su verb - precursor to the modern suru": [POS.SU_VERB],
        POS.COUNTER: [POS.COUNTER],
        POS.NUMERIC: [POS.NUMERIC],

        "noun or verb acting prenominally": [POS.PRENOMINAL],
        "suru verb - special class": [POS.SURU_VERB, POS.SPECIAL_CLASS],
        "ichidan verb - kureru special class": [POS.ICHIDAN_VERB, POS.SPECIAL_CLASS],
        "'taru' adjective": [POS.TARU_ADJECTIVE],
    }

    @classmethod
    def _harmonize(cls, pos: set[str]) -> set[str]:
        result: set[str] = set()
        for item in pos:
            mapped = POSSetManager._remappings.get(item.lower())
            if mapped:
                result.update(mapped)
            else:
                result.add(item)
        return result

    @classmethod
    def _intern_frozenset(cls, pos_values_set: set[str]) -> frozenset[str]:
        """Internal method to intern a harmonized POS set."""
        pos_key = ", ".join(sorted(pos_values_set))
        if pos_key not in POSSetManager._pos_by_str:
            POSSetManager._pos_by_str[string_auto_interner.auto_intern(pos_key)] = frozenset(
                    string_auto_interner.auto_intern_list(list(pos_values_set))
            )
        return POSSetManager._pos_by_str[pos_key]

    @classmethod
    def intern_and_harmonize(cls, pos: str) -> str:
        pos_values_list = ex_str.extract_comma_separated_values(pos).select(lambda it: it.lower()).to_list()
        pos_values_set = POSSetManager._harmonize(set(pos_values_list))
        POSSetManager._intern_frozenset(pos_values_set)
        return ", ".join(sorted(pos_values_set))

    @classmethod
    def intern_and_harmonize_from_list(cls, pos_list: list[str]) -> frozenset[str]:
        """Intern and harmonize POS from a list of strings. Returns the interned frozenset."""
        pos_values_set = POSSetManager._harmonize({pos.lower() for pos in pos_list})
        return POSSetManager._intern_frozenset(pos_values_set)

    @classmethod
    def get(cls, pos: str) -> frozenset[str]: return POSSetManager._pos_by_str[pos]

    @classmethod
    def is_transitive_verb(cls, pos_set: frozenset[str]) -> bool:
        return POS.TRANSITIVE in pos_set

    @classmethod
    def is_intransitive_verb(cls, pos_set: frozenset[str]) -> bool:
        return POS.INTRANSITIVE in pos_set
