from __future__ import annotations
from typing import Callable, Optional, Any

from parsing.universal_dependencies import ud_tree_node_formatter
from parsing.universal_dependencies.core import ud_japanese_part_of_speech_tag, ud_universal_part_of_speech_tag
from parsing.universal_dependencies.core.ud_token import UDToken
from sysutils import kana_utils

class UDTextTreeNode:
    def __init__(self, surface: str, base: str, children: Optional[list[UDTextTreeNode]] = None, tokens: Optional[list[UDToken]] = None) -> None:
        self.surface = surface
        self.base = base if base else surface
        self.tokens:list[UDToken] = tokens if tokens else []
        self.children: list[UDTextTreeNode] = children if children else []
        if tokens:
            self._check_for_inflected_dictionary_phrase()

    def is_morpheme(self) -> bool: return not self.children
    def base_differs_from_surface(self) -> bool:
        return self.base != self.surface

    def is_really_inflected(self) -> bool:
        if self.base == self.surface:
            return False

        if kana_utils.is_only_kana(self.base) != kana_utils.is_only_kana(self.surface):
            return False # some tokenizers do us the favor of finding the kanji representation for some words. That does not equal inflection though.

        return True


    def is_compound(self) -> bool: return len(self.children) > 0

    def is_surface_dictionary_word(self) -> bool:
        from parsing.jamdict_extensions.dict_lookup import DictLookup
        return DictLookup.lookup_word_shallow(self.surface).found_words()

    def base_should_be_shown_separately_in_breakdown(self) -> bool:
        if self.is_morpheme() and self.tokens[0].xpos == ud_japanese_part_of_speech_tag.inflecting_dependent_word:
            return False # todo trying this out. It should get rid of fetching だ for な and such. Not sure what other effects it might have...

        from parsing.jamdict_extensions.dict_lookup import DictLookup
        return self.base_differs_from_surface() and DictLookup.lookup_word_shallow(self.base).found_words()

    def visit(self, callback: Callable[[UDTextTreeNode],None]) -> None:
        callback(self)
        for node in self.children:
            node.visit(callback)

    def __str__(self) -> str: return ud_tree_node_formatter.str_(self, 0)
    def __repr__(self) -> str: return ud_tree_node_formatter.repr_(self, 0)

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, UDTextTreeNode)
                and self.base == other.base
                and self.surface == other.surface
                and self.children == other.children)

    def __hash__(self) -> int: return hash(self.surface)

    #todo this does not feel great. Works for the only case I've found so far, but does not feel great. It might be a better approach to try and ensure that a phrase that ends with inflection get separated from the inflection on the tree level.
    def _check_for_inflected_dictionary_phrase(self) -> None:
        if len(self.tokens) > 2 and self.tokens[-1].xpos == ud_japanese_part_of_speech_tag.inflecting_dependent_word:
            if self.tokens[-2].upos == ud_universal_part_of_speech_tag.verb:
                from parsing.jamdict_extensions.dict_lookup import DictLookup
                candidate_base = "".join(tok.form for tok in self.tokens[:-2]) + self.tokens[-2].lemma
                if DictLookup.lookup_word_shallow(candidate_base).found_words():
                    self.base = candidate_base
