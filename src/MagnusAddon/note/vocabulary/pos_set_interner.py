from __future__ import annotations

from sysutils import ex_str
from sysutils.memory_usage import string_auto_interner


class POSSetManager:
    _pos_by_str: dict[str, frozenset[str]] = {}

    # Maps both JMDict POS names and our own harmonizations to canonical forms
    _remappings: dict[str, list[str]] = {
            # Our own harmonizations (for VocabNote usage)
            "intransitive verb": ["intransitive"],
            "transitive verb": ["transitive"],
            "godan": ["godan verb"],
            "ichidan": ["ichidan verb"],

            # JMDict POS mappings
            "noun or participle which takes the aux. verb suru": ["suru verb"],
            "noun (common) (futsuumeishi)": ["noun"],
            "adjectival nouns or quasi-adjectives (keiyodoshi)": ["na-adjective"],
            "noun, used as a suffix": ["noun", "suffix"],
            "godan verb with 'u' ending": ["godan verb"],
            "godan verb with 'ru' ending": ["godan verb"],
            "godan verb with 'mu' ending": ["godan verb"],
            "godan verb with 'nu' ending": ["godan verb"],
            "godan verb with 'gu' ending": ["godan verb"],
            "godan verb with 'ku' ending": ["godan verb"],
            "godan verb with 'su' ending": ["godan verb"],
            "godan verb with 'bu' ending": ["godan verb"],
            "godan verb with 'u' ending (special class)": ["godan verb", "special-class"],
            "godan verb - -aru special class": ["godan verb", "special-class-aru"],
            "godan verb with 'tsu' ending": ["godan verb"],
            "irregular nu verb": ["nu verb"],
            "godan verb - iku/yuku special class": ["godan verb", "special-class"],
            "godan verb with 'ru' ending (irregular verb)": ["godan verb", "irregular"],
            "ichidan verb": ["ichidan verb"],
            "ichidan verb - zuru verb (alternative form of -jiru verbs)": ["ichidan verb", "zuru verb"],
            "kuru verb - special class": ["kuru verb", "special-class"],
            "yodan verb with 'ru' ending (archaic)": ["yodan verb"],
            "yodan verb with 'ku' ending (archaic)": ["yodan verb"],
            "nidan verb (lower class) with 'ru' ending (archaic)": ["nidan verb"],
            "nidan verb (upper class) with 'ru' ending (archaic)": ["nidan verb"],
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
            "ichidan verb - kureru special class": ["ichidan verb", "special-class"],
            "'taru' adjective": ["taru-adjective"],
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
        return "transitive" in pos_set

    @staticmethod
    def is_intransitive_verb(pos_set: frozenset[str]) -> bool:
        return "intransitive" in pos_set
