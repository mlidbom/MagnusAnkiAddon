from parsing.jamdict_extensions.dict_lookup import DictLookup
from parsing.janome_extensions.parts_of_speech import POS
from parsing.janome_extensions.token_ext import TokenExt
from parsing.tree_parsing import tree_parser
from sysutils import kana_utils


class Node:
    _max_lookahead = 12
    def __init__(self, base: str, surface: str, children=None, tokens: list[TokenExt] = None) -> None:
        self.base = base
        self.surface = surface
        self.tokens = tokens
        self.children:list[Node] = children if children else []

    def __repr__(self) -> str:
        return f"""Node('{self.base}','{self.surface}'{"," + str(self.children) if self.children else ""})"""

    def __eq__(self, other: any) -> bool:
        return (isinstance(other, Node)
                and self.base == other.base
                and self.children == other.children)

    def __hash__(self) -> int:
        return hash(self.surface) + hash(self.children)

    @classmethod
    def create(cls, tokens: list[TokenExt], excluded:set[str]) -> 'Node':
        children = tree_parser._internal_parse(tokens, excluded) if len(tokens) > 1 else None # noqa
        surface = "".join(tok.surface for tok in tokens)
        base = "".join(tok.surface for tok in tokens[:-1]) + tokens[-1].base_form
        surface = surface if base != surface else ""
        return Node(base, surface, children, tokens)

    def get_sentence_display_text(self) -> str:
        return self.surface if self.surface and self.is_verb_compound_not_dictionary_word() else self.base


    def is_base_kana_only(self) -> bool:
        return kana_utils.is_only_kana(self.base)

    def is_surface_kana_only(self) -> bool:
        return self.surface and kana_utils.is_only_kana(self.surface)

    def is_show_base_in_sentence_breakdown(self) -> bool:
        return not self._is_base_manually_excluded()

    def is_show_surface_in_sentence_breakdown(self) -> bool:
        return (self.surface
                and not self.tokens[0].parts_of_speech == POS.Verb.independent
                and not self.tokens[0].parts_of_speech == POS.Verb.non_independent
                and not self._is_surface_manually_excluded()
                and self._is_surface_in_dictionary())

    def _is_surface_in_dictionary(self) -> bool:
        return self.surface and DictLookup.lookup_word_shallow(self.surface).found_words()

    def _is_base_in_dictionary(self) -> bool:
        return self.base and DictLookup.lookup_word_shallow(self.base).found_words()

    def is_verb_compound_not_dictionary_word(self) -> bool:
        if self._is_surface_in_dictionary() or self._is_base_in_dictionary():
            return False

        if not self.children:
            return False

        reversed_tokens = self.tokens[::-1]
        if not reversed_tokens[0].is_verb_auxiliary():
            return False

        for token in reversed_tokens:
            if not token.is_verb_auxiliary():
                return token.is_independent_verb()



    def _is_surface_manually_excluded(self) -> bool:
        if self.base == "ます" and self.surface == "ませ": return True
        if self.base == "です" and self.surface == "でし": return True
        if self.base == "ない" and self.surface == "なく": return True
        return False

    def _is_base_manually_excluded(self) -> bool:
        if self.base == "だ" and self.surface == "な": return True
        if self.base == "だ" and self.surface == "で": return True
        return False