from __future__ import annotations

from sysutils import ex_str
from sysutils.memory_usage import string_auto_interner


class POSSetManager:
    # Canonical POS value constants
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

    _pos_by_str: dict[str, frozenset[str]] = {}

    # Maps both JMDict POS names and our own harmonizations to canonical forms
    _remappings: dict[str, list[str]] = {
            # Our own harmonizations (for VocabNote usage)
        "intransitive verb": [INTRANSITIVE],
        "transitive verb": [TRANSITIVE],
        "godan": [GODAN_VERB],
        "ichidan": [ICHIDAN_VERB],
        
        # JMDict POS mappings
        "noun or participle which takes the aux. verb suru": [SURU_VERB],
        "noun (common) (futsuumeishi)": [NOUN],
        "adjectival nouns or quasi-adjectives (keiyodoshi)": [NA_ADJECTIVE],
        "noun, used as a suffix": [NOUN, SUFFIX],
        "godan verb with 'u' ending": [GODAN_VERB],
        "godan verb with 'ru' ending": [GODAN_VERB],
        "godan verb with 'mu' ending": [GODAN_VERB],
        "godan verb with 'nu' ending": [GODAN_VERB],
        "godan verb with 'gu' ending": [GODAN_VERB],
        "godan verb with 'ku' ending": [GODAN_VERB],
        "godan verb with 'su' ending": [GODAN_VERB],
        "godan verb with 'bu' ending": [GODAN_VERB],
        "godan verb with 'u' ending (special class)": [GODAN_VERB, SPECIAL_CLASS],
        "godan verb - -aru special class": [GODAN_VERB, SPECIAL_CLASS_ARU],
        "godan verb with 'tsu' ending": [GODAN_VERB],
        "irregular nu verb": [NU_VERB],
        "godan verb - iku/yuku special class": [GODAN_VERB, SPECIAL_CLASS],
        "godan verb with 'ru' ending (irregular verb)": [GODAN_VERB, IRREGULAR],
        "ichidan verb": [ICHIDAN_VERB],
        "ichidan verb - zuru verb (alternative form of -jiru verbs)": [ICHIDAN_VERB, ZURU_VERB],
        "kuru verb - special class": [KURU_VERB, SPECIAL_CLASS],
        "yodan verb with 'ru' ending (archaic)": [YODAN_VERB],
        "yodan verb with 'ku' ending (archaic)": [YODAN_VERB],
        "nidan verb (lower class) with 'ru' ending (archaic)": [NIDAN_VERB],
        "nidan verb (upper class) with 'ru' ending (archaic)": [NIDAN_VERB],
        "adjective (keiyoushi)": [I_ADJECTIVE],
        "adjective (keiyoushi) - yoi/ii class": [I_ADJECTIVE],
        "adverb (fukushi)": [ADVERB],
        "adverb taking the 'to' particle": [TO_ADVERB],
        "auxiliary": [AUXILIARY],
        "auxiliary adjective": [I_ADJECTIVE, AUXILIARY],
        "auxiliary verb": [AUXILIARY],
        "conjunction": [CONJUNCTION],
        "copula": [COPULA],
        "expressions (phrases, clauses, etc.)": [EXPRESSION],
        "interjection (kandoushi)": [INTERJECTION],
        "noun, used as a prefix": [PREFIX, NOUN],
        "nouns which may take the genitive case particle 'no'": [NOUN, NO_ADJECTIVE],
        "particle": [PARTICLE],
        "pre-noun adjectival (rentaishi)": [PRE_NOUN_ADJECTIVAL],
        "prefix": [PREFIX],
        "pronoun": [PRONOUN],
        "suffix": [SUFFIX],
        "suru verb - included": [SURU_VERB],
        "suru verb": [SURU_VERB],
        "su verb - precursor to the modern suru": [SU_VERB],
        "counter": [COUNTER],
        "numeric": [NUMERIC],
        "noun or verb acting prenominally": [PRENOMINAL],
        "suru verb - special class": [SURU_VERB, SPECIAL_CLASS],
        "ichidan verb - kureru special class": [ICHIDAN_VERB, SPECIAL_CLASS],
        "'taru' adjective": [TARU_ADJECTIVE],
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
        return POSSetManager.TRANSITIVE in pos_set

    @staticmethod
    def is_intransitive_verb(pos_set: frozenset[str]) -> bool:
        return POSSetManager.INTRANSITIVE in pos_set
