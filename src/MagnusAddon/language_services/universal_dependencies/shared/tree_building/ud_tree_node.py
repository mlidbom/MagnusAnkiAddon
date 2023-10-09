from __future__ import annotations

from typing import Callable

from language_services.universal_dependencies.shared.tokenizing import xpos, ud_universal_part_of_speech_tag
from language_services.universal_dependencies.shared.tokenizing.ud_token import UDToken
from language_services.universal_dependencies.shared.tree_building import ud_tree_node_formatter
from sysutils import kana_utils

class UDTreeNode:
    def __init__(self, depth: int, children: list[UDTreeNode], tokens: list[UDToken]) -> None:
        self.depth = depth
        self.form = "".join(tok.form for tok in tokens)
        self.tokens = tokens
        self.children = children
        self.norm = self.build_norm()
        self.lemma = self.build_lemma()

    def lemma_differs_from_form(self) -> bool:
        return self.lemma != self.form

    def is_really_inflected(self) -> bool:
        if self.lemma == self.form:
            return False

        if kana_utils.is_only_kana(self.lemma) != kana_utils.is_only_kana(self.form):
            return False  # some tokenizers do us the favor of finding the kanji representation for some words. That does not equal inflection though.

        return True

    def is_morpheme(self) -> bool: return not self.is_compound()
    def is_compound(self) -> bool: return len(self.tokens) > 1

    def is_form_dictionary_word(self) -> bool:
        from language_services.jamdict_ex.dict_lookup import DictLookup
        return DictLookup.lookup_word_shallow(self.form).found_words()

    def form_should_be_shown_in_breakdown(self) -> bool:
        if self.is_morpheme():
            if self.tokens[0].upos == ud_universal_part_of_speech_tag.verb and self.lemma_differs_from_form():
                return False
            if self.is_excluded_surface(self.tokens[0]):
                return False


        return self.is_form_dictionary_word()

    def lemma_should_be_shown_in_breakdown(self) -> bool:
        from language_services.jamdict_ex.dict_lookup import DictLookup
        return self.lemma_differs_from_form() and DictLookup.lookup_word_shallow(self.lemma).found_words()

    def visit(self, callback: Callable[[UDTreeNode], None]) -> None:
        callback(self)
        for node in self.children:
            node.visit(callback)

    def __str__(self) -> str: return ud_tree_node_formatter.str_(self, 0)

    def _node_appears_to_be_inflected_phrase(self) -> bool:
        return (len(self.tokens) > 2
                and self.tokens[-1].xpos == xpos.inflecting_dependent_word
                and self.tokens[-2].upos == ud_universal_part_of_speech_tag.verb)

    def build_norm(self) -> str:
        if self.is_compound(): return ""

        if self.is_excluded_norm(self.tokens[0]):
            return self.form

        return self.tokens[0].norm

    def build_lemma(self) -> str:
        if self.is_morpheme() and not self.is_excluded_lemma(self.tokens[0]):
            return self.tokens[0].lemma

        if self._node_appears_to_be_inflected_phrase():
            from language_services.jamdict_ex.dict_lookup import DictLookup
            candidate_lemma = "".join(tok.form for tok in self.tokens[:-2]) + self.tokens[-2].lemma
            if DictLookup.lookup_word_shallow(candidate_lemma).found_words():
                return candidate_lemma

        return self.form

    @staticmethod
    def is_excluded_surface(token: UDToken) -> bool:
        return (token.xpos, token.form, token.lemma) in _excluded_surfaces

    @staticmethod
    def is_excluded_lemma(token: UDToken) -> bool:
        return (token.xpos, token.form, token.lemma) in _excluded_lemmas

    @staticmethod
    def is_excluded_norm(token: UDToken) -> bool:
        return (token.xpos, token.form, token.norm) in _excluded_norms

# It would be nice to find a logical pattern rather than hardcoded exclusions, but nothing has turned up yet
_excluded_surfaces = {
    (xpos.inflecting_dependent_word, "て", "てる"),
}

_excluded_lemmas = {
    (xpos.inflecting_dependent_word, "たら", "た"),
    (xpos.inflecting_dependent_word, "に", "だ"),
    (xpos.inflecting_dependent_word, "な", "だ"),
    (xpos.inflecting_dependent_word, "だろう", "だ"),
    (xpos.inflecting_dependent_word, "だろ", "だ"),
}

_excluded_norms = _excluded_lemmas
