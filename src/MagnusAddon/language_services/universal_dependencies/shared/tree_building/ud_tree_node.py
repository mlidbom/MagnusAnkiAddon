from __future__ import annotations
from typing import Callable, Optional, Any

from language_services.universal_dependencies.shared.tree_building import ud_tree_node_formatter
from language_services.universal_dependencies.shared.tokenizing import ud_japanese_part_of_speech_tag, ud_universal_part_of_speech_tag
from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from sysutils import kana_utils

class UDTreeNode:
    def __init__(self, surface: str, base: str, children: Optional[list[UDTreeNode]] = None, tokens: Optional[list[UDToken]] = None) -> None:
        self.surface = surface
        self.lemma = base if base else surface
        self.tokens:list[UDToken] = tokens if tokens else []
        self.children: list[UDTreeNode] = children if children else []
        if tokens:
            self._check_for_inflected_dictionary_phrase()

    def is_morpheme(self) -> bool: return not self.children
    def base_differs_from_surface(self) -> bool:
        return self.lemma != self.surface

    def is_really_inflected(self) -> bool:
        if self.lemma == self.surface:
            return False

        if kana_utils.is_only_kana(self.lemma) != kana_utils.is_only_kana(self.surface):
            return False # some tokenizers do us the favor of finding the kanji representation for some words. That does not equal inflection though.

        return True


    def is_compound(self) -> bool: return len(self.children) > 0

    def is_surface_dictionary_word(self) -> bool:
        from language_services.jamdict_ex.dict_lookup import DictLookup
        return DictLookup.lookup_word_shallow(self.surface).found_words()

    def base_should_be_shown_separately_in_breakdown(self) -> bool:
        if self.is_morpheme() and self.tokens[0].xpos == ud_japanese_part_of_speech_tag.inflecting_dependent_word:
            return False # todo trying this out. It should get rid of fetching だ for な and such. Not sure what other effects it might have...

        from language_services.jamdict_ex.dict_lookup import DictLookup
        return self.base_differs_from_surface() and DictLookup.lookup_word_shallow(self.lemma).found_words()

    def visit(self, callback: Callable[[UDTreeNode],None]) -> None:
        callback(self)
        for node in self.children:
            node.visit(callback)

    def __str__(self) -> str: return ud_tree_node_formatter.str_(self, 0)
    def __repr__(self) -> str: return ud_tree_node_formatter.repr_(self, 0)

    def __eq__(self, other: Any) -> bool:
        return (isinstance(other, UDTreeNode)
                and self.lemma == other.lemma
                and self.surface == other.surface
                and self.children == other.children)

    def __hash__(self) -> int: return hash(self.surface)

    #todo this does not feel great. Works for the only case I've found so far, but does not feel great. It might be a better approach to try and ensure that a phrase that ends with inflection get separated from the inflection on the tree level.
    def _check_for_inflected_dictionary_phrase(self) -> None:
        if len(self.tokens) > 2 and self.tokens[-1].xpos == ud_japanese_part_of_speech_tag.inflecting_dependent_word:
            if self.tokens[-2].upos == ud_universal_part_of_speech_tag.verb:
                from language_services.jamdict_ex.dict_lookup import DictLookup
                candidate_base = "".join(tok.form for tok in self.tokens[:-2]) + self.tokens[-2].lemma
                if DictLookup.lookup_word_shallow(candidate_base).found_words():
                    self.lemma = candidate_base
