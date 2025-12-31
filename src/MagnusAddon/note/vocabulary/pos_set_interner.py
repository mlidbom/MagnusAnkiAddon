from __future__ import annotations

from sysutils import ex_str
from sysutils.memory_usage import string_auto_interner


class POS:
    """Canonical POS (Part of Speech) value constants."""
    TRANSITIVE: str = "transitive"
    INTRANSITIVE: str = "intransitive"
    GODAN_VERB: str = "godan verb"
    ICHIDAN_VERB: str = "ichidan verb"
    SURU_VERB: str = "suru verb"
    KURU_VERB: str = "kuru verb"
    NU_VERB: str = "nu verb"
    SU_VERB: str = "su verb"
    YODAN_VERB: str = "yodan verb"
    NIDAN_VERB: str = "nidan verb"
    NOUN: str = "noun"
    NA_ADJECTIVE: str = "na-adjective"
    I_ADJECTIVE: str = "i-adjective"
    TARU_ADJECTIVE: str = "taru-adjective"
    ADVERB: str = "adverb"
    TO_ADVERB: str = "to-adverb"
    EXPRESSION: str = "expression"
    AUXILIARY: str = "auxiliary"
    CONJUNCTION: str = "conjunction"
    COPULA: str = "copula"
    INTERJECTION: str = "interjection"
    PARTICLE: str = "particle"
    PREFIX: str = "prefix"
    SUFFIX: str = "suffix"
    PRONOUN: str = "pronoun"
    COUNTER: str = "counter"
    NUMERIC: str = "numeric"
    PRENOMINAL: str = "prenominal"
    PRE_NOUN_ADJECTIVAL: str = "pre-noun-adjectival"
    NO_ADJECTIVE: str = "no-adjective"
    SPECIAL_CLASS: str = "special-class"
    SPECIAL_CLASS_ARU: str = "special-class-aru"
    ZURU_VERB: str = "zuru verb"
    IRREGULAR: str = "irregular"
    UNKNOWN: str = "Unknown"


class POSSetManager:
    _pos_by_str: dict[str, frozenset[str]] = {}

    # Maps both JMDict POS names and our own harmonizations to canonical forms
    _remappings: dict[str, list[str]] = {
        # Our own harmonizations (for VocabNote usage)
        "intransitive verb": [POS.INTRANSITIVE],
        "transitive verb": [POS.TRANSITIVE],
        "godan": [POS.GODAN_VERB],
        "ichidan": [POS.ICHIDAN_VERB],

        # JMDict POS mappings
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
        "auxiliary": [POS.AUXILIARY],
        "auxiliary adjective": [POS.I_ADJECTIVE, POS.AUXILIARY],
        "auxiliary verb": [POS.AUXILIARY],
        "conjunction": [POS.CONJUNCTION],
        "copula": [POS.COPULA],
        "expressions (phrases, clauses, etc.)": [POS.EXPRESSION],
        "interjection (kandoushi)": [POS.INTERJECTION],
        "noun, used as a prefix": [POS.PREFIX, POS.NOUN],
        "nouns which may take the genitive case particle 'no'": [POS.NOUN, POS.NO_ADJECTIVE],
        "particle": [POS.PARTICLE],
        "pre-noun adjectival (rentaishi)": [POS.PRE_NOUN_ADJECTIVAL],
        "prefix": [POS.PREFIX],
        "pronoun": [POS.PRONOUN],
        "suffix": [POS.SUFFIX],
        "suru verb - included": [POS.SURU_VERB],
        "suru verb": [POS.SURU_VERB],
        "su verb - precursor to the modern suru": [POS.SU_VERB],
        "counter": [POS.COUNTER],
        "numeric": [POS.NUMERIC],
        "noun or verb acting prenominally": [POS.PRENOMINAL],
        "suru verb - special class": [POS.SURU_VERB, POS.SPECIAL_CLASS],
        "ichidan verb - kureru special class": [POS.ICHIDAN_VERB, POS.SPECIAL_CLASS],
        "'taru' adjective": [POS.TARU_ADJECTIVE],
    }

    @staticmethod
    def _harmonize(pos: set[str]) -> set[str]:
        result: set[str] = set()
        for item in pos:
            mapped = POSSetManager._remappings.get(item.lower())
            if mapped:
                result.update(mapped)
            else:
                result.add(item)
        return result

    @staticmethod
    def _intern_frozenset(pos_values_set: set[str]) -> frozenset[str]:
        """Internal method to intern a harmonized POS set."""
        pos_key = ", ".join(sorted(pos_values_set))
        if pos_key not in POSSetManager._pos_by_str:
            POSSetManager._pos_by_str[string_auto_interner.auto_intern(pos_key)] = frozenset(
                    string_auto_interner.auto_intern_list(list(pos_values_set))
            )
        return POSSetManager._pos_by_str[pos_key]

    @staticmethod
    def intern_and_harmonize(pos: str) -> str:
        pos_values_list = ex_str.extract_comma_separated_values(pos).select(lambda it: it.lower()).to_list()
        pos_values_set = POSSetManager._harmonize(set(pos_values_list))
        POSSetManager._intern_frozenset(pos_values_set)
        return ", ".join(sorted(pos_values_set))

    @staticmethod
    def intern_and_harmonize_from_list(pos_list: list[str]) -> frozenset[str]:
        """Intern and harmonize POS from a list of strings. Returns the interned frozenset."""
        pos_values_set = POSSetManager._harmonize({pos.lower() for pos in pos_list})
        return POSSetManager._intern_frozenset(pos_values_set)

    @staticmethod
    def get(pos: str) -> frozenset[str]: return POSSetManager._pos_by_str[pos]

    @staticmethod
    def contains(pos_set: frozenset[str], value: str) -> bool:
        """Check if a harmonized value is in the POS set."""
        return value in pos_set

    @staticmethod
    def is_transitive_verb(pos_set: frozenset[str]) -> bool:
        return POS.TRANSITIVE in pos_set

    @staticmethod
    def is_intransitive_verb(pos_set: frozenset[str]) -> bool:
        return POS.INTRANSITIVE in pos_set
