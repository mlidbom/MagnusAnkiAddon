from parsing.jamdict_extensions.dict_lookup import DictLookup
from parsing.janome_extensions.parts_of_speech import POS, PartsOfSpeech
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
        children = tree_parser._internal_parse(tokens, excluded) if len(tokens) > 1 else [] # tree_parser._find_compounds(tokens[0], excluded) # noqa
        return cls.create_non_recursive(tokens, children)

    @classmethod
    def create_non_recursive(cls, tokens: list[TokenExt], children:list['Node'] = None) -> 'Node':
        children = children if children else []
        surface = "".join(tok.surface for tok in tokens)
        base = "".join(tok.surface for tok in tokens[:-1]) + tokens[-1].base_form
        surface = surface if base != surface else ""
        return Node(base, surface, children, tokens)

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

    def is_verb_compound(self) -> bool:
        if not self.children:
            return False

        reversed_tokens = self.tokens[::-1]
        if not reversed_tokens[0].is_verb_auxiliary():
            return False

        for token in reversed_tokens:
            if not token.is_verb_auxiliary():
                return token.is_independent_verb()
        
        return True

    def _is_surface_manually_excluded(self) -> bool:
        global excluded_surface_pos
        pos = self.tokens[0].parts_of_speech

        if (self.base == "ます" and self.surface == "ませ"
                or self.base == "です" and self.surface == "でし"
                or self.base == "たい" and self.surface == "たく"
                or self.base == "ている" and self.surface == "てい"
                or self.base == "ない" and self.surface == "なく"):
            excluded_surface_pos.add(pos)
            return True
        return False

    def _is_base_manually_excluded(self) -> bool:
        global excluded_base_pos
        pos = self.tokens[0].parts_of_speech

        if (self.base == "だ" and self.surface == "な"
                or self.base == "だ" and self.surface == "で"
                or self.base == "た" and self.surface == "たら"):
            excluded_base_pos.add(pos)
            return True
        return False

    def get_priority_class(self, question) -> str:
        if question != self.surface and question != self.base:
            return ""

        if question == self.surface and question in _Statics.low_priority_surfaces:
            return _Statics.Class.low
        if question == self.base and question in _Statics.low_priority_bases:
            return _Statics.Class.low

        if not self.children:
            if all(token.is_verb_auxiliary() for token in self.tokens):
                return _Statics.Class.low

        return ""

class _Statics:
    class Class:
        low = "word_priority_low"

    low_priority_surfaces: set[str] = set()
    low_priority_bases: set[str] = set("しもよかとたてでをなのにだがは") | {"する", "です", "私"}

excluded_surface_pos: set[PartsOfSpeech] = set()
excluded_base_pos: set[PartsOfSpeech] = set()