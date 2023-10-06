from __future__ import annotations
from typing import Callable, Optional, Any

from language_services.jamdict_ex.dict_lookup import DictLookup
from language_services.janome_ex.tokenizing.jn_parts_of_speech import POS
from language_services.janome_ex.tokenizing.jn_token import JNToken
from language_services.janome_ex.tree_building import jn_tree_builder
from sysutils import kana_utils


class TreeParserNode:
    _max_lookahead = 12
    def __init__(self, surface: str, base: str, children: Optional[list[TreeParserNode]] = None, tokens: Optional[list[JNToken]] = None) -> None:
        self.surface = surface
        self.base = base if base else surface
        self.tokens = tokens if tokens else []
        self.children:list[TreeParserNode] = children if children else []

    def _children_repr(self, level:int = 1) -> str:
        if not self.children:
            return ""
        indent = "  " * level
        children_string = ', '.join(child._repr(level) for child in self.children)
        return f""",[\n{indent}{children_string}]"""

    def _repr(self, level: int) -> str:
        return f"""N('{self.surface}', '{self.base if self.is_inflected() else ""}'{self._children_repr(level + 1)})"""

    def __repr__(self) -> str:
        return self._repr(0)

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, TreeParserNode)
                and self.base == other.base
                and self.surface == other.surface
                and self.children == other.children)

    def __hash__(self) -> int:
        return hash(self.surface) + hash(self.children)

    def is_inflected(self) -> bool: return self.base != self.surface

    @classmethod
    def create(cls, tokens: list[JNToken], excluded:set[str]) -> TreeParserNode:
        children = jn_tree_builder._recursing_parse(tokens, excluded) if len(tokens) > 1 else [] # jn_tree_builder._find_compounds(tokens[0], excluded) # noqa
        return cls.create_non_recursive(tokens, children)

    @classmethod
    def create_non_recursive(cls, tokens: list[JNToken], children: Optional[list[TreeParserNode]] = None) -> TreeParserNode:
        children = children if children else []
        surface = "".join(tok.surface for tok in tokens)
        base = "".join(tok.surface for tok in tokens[:-1]) + tokens[-1].base_form
        return TreeParserNode(surface, base, children, tokens)

    def is_base_kana_only(self) -> bool:
        return kana_utils.is_only_kana(self.base)

    def is_surface_kana_only(self) -> bool:
        return kana_utils.is_only_kana(self.surface)

    def is_show_at_all_in_sentence_breakdown(self) -> bool:
        return self.is_show_base_in_sentence_breakdown() or self.is_show_surface_in_sentence_breakdown()

    def is_show_base_in_sentence_breakdown(self) -> bool:
        return not self._is_base_manually_excluded()

    def is_show_surface_in_sentence_breakdown(self) -> bool:
        return (self.is_inflected()
                and not self.tokens[0].parts_of_speech == POS.Verb.independent
                and not self.tokens[0].parts_of_speech == POS.Verb.dependent
                and not self._is_surface_manually_excluded()
                and self._is_surface_in_dictionary())

    def _is_surface_in_dictionary(self) -> bool:
        return DictLookup.lookup_word_shallow(self.surface).found_words()

    def _is_inflected_and_base_is_in_dictionary(self) -> bool:
        return self.is_inflected() and DictLookup.lookup_word_shallow(self.base).found_words()

    def is_probably_not_dictionary_word(self) -> bool:
        verb_index = next((i for i, item in enumerate(self.tokens) if jn_tree_builder.is_verb([item])), -1)
        if -1 < verb_index < len(self.tokens) - 1:
            if jn_tree_builder.is_verb_auxiliary(self.tokens[verb_index + 1:]):
                if not self._is_inflected_and_base_is_in_dictionary():
                    return True
        
        return False

    def is_dictionary_word(self, display_text: str) -> bool:
        if self.is_inflected() and display_text == self.base and self._is_inflected_and_base_is_in_dictionary():
            return True
        if display_text == self.surface and self._is_surface_in_dictionary():
            return True

        return False

    def _is_surface_manually_excluded(self) -> bool:
        if (self.base == "ます" and self.surface == "ませ"
                or self.base == "です" and self.surface == "でし"
                or self.base == "たい" and self.surface == "たく"
                or self.base == "ている" and self.surface == "てい"
                or self.base == "ない" and self.surface == "なく"):
            return True
        return False

    def _is_base_manually_excluded(self) -> bool:
        if (self.base == "だ" and self.surface == "な"
                or self.base == "だ" and self.surface == "で"
                or self.base == "た" and self.surface == "たら"):
            return True
        return False

    def get_priority_class(self, question: str, highlighted:set[str]) -> str:
        if question in highlighted:
            return priorities.very_high

        if question != self.surface and question != self.base:
            return priorities.unknown

        kanji_count = len([char for char in self.surface if not kana_utils.is_kana(char)])

        #todo: if this works out well, remove the code with hard coded values below
        if kanji_count == 0:
            if len(self.surface) == 1:
                return priorities.very_low
            if len(self.surface) == 2:
                return priorities.low

        if question == self.surface:
            if question in _Statics.hard_coded_surface_priorities:
                return _Statics.hard_coded_surface_priorities[question]
        if question == self.base:
            if question in _Statics.hard_coded_base_priorities:
                return _Statics.hard_coded_base_priorities[question]

        if kanji_count > 1:
            return priorities.high

        return priorities.medium

    def visit(self, callback: Callable[[TreeParserNode],None]) -> None:
        callback(self)
        for node in self.children:
            node.visit(callback)

class Priorities:
    def __init__(self) -> None:
        self.unknown = "unknown"
        self.very_low = "very_low"
        self.low = "low"
        self.medium = "medium"
        self.high = "high"
        self.very_high = "very_high"

priorities = Priorities()


class _Statics:
    hard_coded_base_priorities: dict[str, str] = dict()
    hard_coded_surface_priorities: dict[str, str] = dict()

    lowest_priority_surfaces: set[str] = set()
    # for particle in "しもよかとたてでをなのにだがは": hard_coded_base_priorities[particle] = priorities.very_low
    # for word in "する|です|私|なる|この|あの|その|いる|ある".split("|"): hard_coded_base_priorities[word] = priorities.low